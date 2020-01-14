from django.urls import path

from projects import views
app_name = "projects"

urlpatterns = [
    path("", views.list, name="list"),
    path("milestones/<id>/", views.milestone, name="milestone"),
    path("applications/<id>/", views.application, name="applications"),
    path("tasks", views.tasks, name="tasks")
]