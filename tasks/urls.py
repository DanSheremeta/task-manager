from django.urls import path

from tasks.views import (
    TaskListView,
    WorkerTaskListView,
    WorkerDetailView,
    WorkerUpdateView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerRegistrationView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("mytasks/", WorkerTaskListView.as_view(), name="worker-task-list"),
    path("profile/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("profile/<int:pk>/change/", WorkerUpdateView.as_view(), name="worker-update"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("register/", WorkerRegistrationView.as_view(), name="worker-registration"),
]

app_name = "tasks"
