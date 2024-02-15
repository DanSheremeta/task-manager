from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tasks.forms import WorkerUpdateForm
from tasks.models import Task, Position, TaskType


class WorkerViewsTest(TestCase):
    def setUp(self):
        position = self.position = Position.objects.create(name="Front-end Developer")
        user = self.user = get_user_model().objects.create_user(
            username="testuser", position=position, password="password1"
        )

        task_type = TaskType.objects.create(name="Test type")
        statuses = ("to_do", "in_progress", "reviewing", "completed")
        priorities = ("low", "medium", "high", "high")

        for status, priority, i in zip(statuses, priorities, range(1, 5)):
            task = Task.objects.create(
                name=f"Task {i}",
                description="Task description",
                deadline=datetime(2024, 4, 4),
                status=status,
                priority=priority,
                task_type=task_type,
            )
            task.assignees.add(user)

        self.client.force_login(user)

    def test_worker_task_list_view(self):
        response = self.client.get(reverse("tasks:worker-task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_list", response.context)
        task_list = response.context["task_list"]
        self.assertEqual(task_list.count(), 4)

    def test_worker_detail_view(self):
        response = self.client.get(
            reverse("tasks:worker-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.user)

    def test_worker_update_view(self):
        response = self.client.get(
            reverse("tasks:worker-update", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], WorkerUpdateForm)

    def test_worker_registration_view_get(self):
        response = self.client.get(reverse("tasks:worker-registration"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("positions", response.context)
        positions = response.context["positions"]
        self.assertEqual(len(positions), 1)

    def test_worker_registration_view_post(self):
        data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "test@example.com",
            "position": self.position.id,
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        response = self.client.post(reverse("tasks:worker-registration"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())
