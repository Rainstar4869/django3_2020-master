from django.urls import path
from . import views

app_name = "upload"

urlpatterns = [
    path("", views.image_upload, name="image_upload"),
    path("index/", views.index, name="image_upload_index"),
]
