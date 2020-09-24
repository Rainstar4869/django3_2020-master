from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path("students/", views.StudentAPI.as_view(), name="students"),
]
