from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views import View

from tasks.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskForm,
    TaskNameSearchForm,
)
from tasks.models import Task, Position


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskListView(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class WorkerTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerTaskListView, self).get_context_data(**kwargs)
        context["only_current_user"] = True
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
        return reverse_lazy(
            "tasks:worker-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def get_object(self, queryset=None):
        return self.request.user


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerRegistrationView(View):
    template_name = "tasks/worker_form.html"

    def get(self, request, *args, **kwargs):
        positions = Position.objects.all()
        form = WorkerCreationForm()
        return render(
            request,
            self.template_name,
            {"form": form, "positions": positions}
        )

    def post(self, request, *args, **kwargs):
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            position_id = request.POST.get('position')
            position = Position.objects.get(pk=position_id)
            user = form.save(commit=False)
            user.position = position
            user.save()
            login(request, user)
            return redirect("tasks:task-list")
        else:
            positions = Position.objects.all()
            return render(
                request,
                self.template_name,
                {"form": form, "positions": positions}
            )
