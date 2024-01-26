from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        related_name="workers",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _("worker")
        verbose_name_plural = _("workers")
        ordering = ("username",)

    def __str__(self):
        return (f"{self.position} {self.username}"
                f" ({self.first_name} {self.last_name})")


class TaskType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
    )
    task_type = models.ForeignKey(
        TaskType,
        related_name="tasks",
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
    )

    class Meta:
        ordering = ("-deadline", "priority",)
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def __str__(self):
        return (f"{self.name} ({self.task_type},"
                f"{self.priority} priority)")
