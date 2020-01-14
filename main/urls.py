from django.urls import path

app_name = "main"
from main import views

urlpatterns = [
    path("",  views.index, name="home"),
    path("dashboard",  views.dashboard, name="dashboard")
]