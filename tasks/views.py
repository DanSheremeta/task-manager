from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from tasks.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 10
