from django.contrib.auth.forms import UserCreationForm

from tasks.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "email",
            "first_name",
            "last_name",
        )
