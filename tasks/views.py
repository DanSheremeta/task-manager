from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views import View

from tasks.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    WorkerLoginForm,
    TaskForm,
    TaskNameSearchForm,
)
from tasks.models import Position, Task

from django.views.generic import TemplateView
from django.db.models import Count


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["workers"] = (
            get_user_model().objects.all().prefetch_related("tasks__task_type")
        )

        tasks_status_count = (
            Task.objects.values("status")
            .annotate(total=Count("status"))
            .order_by("status")
        )
        tasks_priority_count = (
            Task.objects.values("priority")
            .annotate(total=Count("priority"))
            .order_by("priority")
        )

        context["tasks_status_count"] = {
            task["status"]: task["total"] for task in tasks_status_count
        }
        context["tasks_priority_count"] = {
            task["priority"]: task["total"] for task in tasks_priority_count
        }
        context["tasks_count"] = Task.objects.count()

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskListView(initial={"name": name})
        context["statuses"] = [
            ("to_do", "#7d73d0", "To Do"),
            ("in_progress", "#7696d9", "In Progress"),
            ("reviewing", "#5eb4c2", "Reviewing"),
            ("completed", "#5ab090", "Completed"),
        ]
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.kwargs["pk"]})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerTaskListView, self).get_context_data(**kwargs)
        context["only_current_user"] = True
        context["statuses"] = [
            ("to_do", "#7d73d0", "To Do"),
            ("in_progress", "#7696d9", "In Progress"),
            ("reviewing", "#5eb4c2", "Reviewing"),
            ("completed", "#5ab090", "Completed"),
        ]
        return context

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.all().prefetch_related("tasks__task_type")
    template_name = "tasks/worker_detail.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    template_name = "tasks/worker_form.html"

    def get_success_url(self):
        return reverse_lazy("tasks:worker-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        obj = super(WorkerUpdateView, self).get_object(queryset=queryset)

        if obj != self.request.user:
            raise PermissionDenied(
                "You don't have permission to update info about this worker!"
            )
        return obj


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        _id = self.request.user.id
        context["to_do"] = Task.objects.all()
        context["in_progress"] = Task.objects.filter(status="in_progress")
        context["reviewing"] = Task.objects.filter(status="reviewing")
        context["completed"] = Task.objects.filter(status="completed")
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class WorkerRegistrationView(View):
    template_name = "tasks/worker_form.html"

    def get(self, request, *args, **kwargs):
        positions = Position.objects.all()
        form = WorkerCreationForm()
        return render(
            request, self.template_name, {"form": form, "positions": positions}
        )

    def post(self, request, *args, **kwargs):
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            position_id = request.POST.get("position")
            position = Position.objects.get(pk=position_id)
            user = form.save(commit=False)
            user.position = position
            user.save()
            auth_login(request, user)
            return redirect("tasks:task-list")
        else:
            positions = Position.objects.all()
            return render(
                request, self.template_name, {"form": form, "positions": positions}
            )


class WorkerLoginView(LoginView):
    authentication_form = WorkerLoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("tasks:home")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me is True:
            self.request.session.set_expiry(60 * 60 * 24 * 14)  # 14 days
        else:
            self.request.session.set_expiry(0)  # After closing browser

        auth_login(self.request, form.get_user())
        return super().form_valid(form)
