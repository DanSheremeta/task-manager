from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render, redirect
from django.views import View

from tasks.forms import WorkerCreationForm
from tasks.models import Task, Position


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 10


class WorkerRegistrationView(View):
    template_name = "registration/worker_registration.html"

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
