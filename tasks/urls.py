from django.urls import path

from tasks.views import (
    TaskListView,
    WorkerRegistrationView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("register/", WorkerRegistrationView.as_view(), name="worker-registration"),
]

app_name = "tasks"
