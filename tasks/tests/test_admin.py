from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from tasks.admin import WorkerAdmin, TaskAdmin
from tasks.models import Worker, Position, Task


class WorkerAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.position = Position.objects.create(name="Position 1")

    def setUp(self):
        self.admin_site = AdminSite()

    def test_worker_admin_list_display(self):
        worker_admin = WorkerAdmin(Worker, self.admin_site)
        self.assertIn("position", worker_admin.list_display)

    def test_worker_admin_fieldsets(self):
        worker_admin = WorkerAdmin(Worker, self.admin_site)
        fieldsets = worker_admin.get_fieldsets(None, self.user)
        self.assertTrue(
            any("position" in fieldset[1]["fields"] for fieldset in fieldsets)
        )

    def test_worker_admin_add_fieldsets(self):
        worker_admin = WorkerAdmin(Worker, self.admin_site)
        add_fieldsets = worker_admin.get_fieldsets(None, self.user)
        self.assertTrue(
            any("position" in fieldset[1]["fields"] for fieldset in add_fieldsets)
        )


class TaskAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()

    def test_task_admin_search_fields(self):
        task_admin = TaskAdmin(Task, self.admin_site)
        self.assertIn("name", task_admin.search_fields)
        self.assertIn("task_type", task_admin.search_fields)
        self.assertIn("priority", task_admin.search_fields)

    def test_task_admin_list_filter(self):
        task_admin = TaskAdmin(Task, self.admin_site)
        self.assertIn("deadline", task_admin.list_filter)
        self.assertIn("priority", task_admin.list_filter)
