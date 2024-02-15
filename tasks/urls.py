from django.urls import path
from django.contrib.auth import views as auth_views

from tasks.views import (
    TaskListView,
    WorkerTaskListView,
    WorkerRegistrationView,
    WorkerDetailView,
    WorkerUpdateView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    HomePageView, WorkerLoginView,
)

urlpatterns = [
    # Home url
    path("", HomePageView.as_view(), name="home"),

    # Tasks urls
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # Worker urls
    path("mytasks/", WorkerTaskListView.as_view(), name="worker-task-list"),
    path("profile/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("profile/<int:pk>/change/", WorkerUpdateView.as_view(), name="worker-update"),
    path("register/", WorkerRegistrationView.as_view(), name="registration"),
    path("login/", WorkerLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
]

app_name = "tasks"
