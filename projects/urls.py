from django.urls import path

from projects import views
app_name = "projects"

urlpatterns = [
    path("", views.list, name="list"),
    path("create/", views.project_create, name="project_create"),
    path("edit/<int:pk>/", views.project_edit, name="project_edit"),
    path("delete/<int:pk>/", views.project_delete, name="project_delete"),
    path("milestones/<id>/", views.milestone, name="milestone"),
    path("applications/<id>/", views.application, name="applications"),
    path("tasks", views.tasks, name="tasks")
]