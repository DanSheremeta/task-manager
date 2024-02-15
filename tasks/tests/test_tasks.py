from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.forms import TaskForm
from tasks.models import Task, TaskType, Position


class TaskViewsTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="Designer")
        user = self.user1 = get_user_model().objects.create_user(
            username="user1", position=position, password="password1"
        )

        self.client.force_login(user)

        task_type = TaskType.objects.create(name="Test task type")
        statuses = ("to_do", "in_progress", "reviewing", "completed") * 2
        priorities = ("low", "medium", "high", "low") * 2

        self.task0 = Task.objects.create(
            name="Task 0",
            description="Task description",
            deadline=datetime(2024, 4, 4),
            status="to_do",
            priority="low",
            task_type=task_type,
        )

        for status, priority, i in zip(statuses, priorities, range(1, 9)):
            Task.objects.create(
                name=f"Task {i}",
                description="Task description",
                deadline=datetime(2024, 4, 4),
                status=status,
                priority=priority,
                task_type=task_type,
            )

    def test_home_page_view(self):
        response = self.client.get(reverse("tasks:home"))
        tasks_status_count = response.context["tasks_status_count"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("workers", response.context)
        self.assertIn("tasks_count", response.context)
        self.assertIn("tasks_status_count", response.context)
        self.assertEqual(tasks_status_count["to_do"], 3)
        self.assertEqual(tasks_status_count["in_progress"], 2)
        self.assertEqual(tasks_status_count["reviewing"], 2)
        self.assertEqual(tasks_status_count["completed"], 2)

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("task_list", response.context)
        self.assertIn("search_form", response.context)
        self.assertIn("statuses", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 6)

    def test_task_name_search(self):
        response = self.client.get(reverse("tasks:task-list") + "?name=2")
        self.assertEqual(response.status_code, 200)
        task_list = response.context["task_list"]
        self.assertEqual(len(task_list), 1)
        self.assertNotIn("Task 5", [task.name for task in task_list])

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("tasks:task-detail", kwargs={"pk": self.task0.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.task0)
        self.assertIn("to_do", response.context)
        self.assertIn("in_progress", response.context)
        self.assertIn("reviewing", response.context)
        self.assertIn("completed", response.context)

    def test_task_create_view(self):
        response = self.client.get(reverse("tasks:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_task_update_view(self):
        response = self.client.get(
            reverse("tasks:task-update", kwargs={"pk": self.task0.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_task_delete_view(self):
        response = self.client.get(
            reverse("tasks:task-delete", kwargs={"pk": self.task0.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("submit", response.content.decode("utf-8"))

    def test_task_delete_view_post(self):
        response = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": self.task0.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task0.pk).exists())
