from django.urls import path

from fund import views
app_name = "fund"

urlpatterns = [
    path("", views.list, name="list"),
    path("add", views.add_fund, name="add"),
    path("view/<id>/", views.view, name="view"),
]