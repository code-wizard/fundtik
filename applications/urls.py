from django.urls import path

from applications import views
app_name = "applications"

urlpatterns = [
    path("", views.list, name="list"),
    path("edit/<id>/", views.edit, name="edit")
]