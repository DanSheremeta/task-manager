from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# test text for testing new branch
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
