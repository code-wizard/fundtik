from django.urls import path
from filemanager import views

app_name = "filemanager"

urlpatterns = [
    path("files", views.files, name="files")
]