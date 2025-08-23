from django.urls import path
from . import views
app_name = "staff"
urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    path('edit/<int:pk>/', views.staff_edit, name='staff_edit'),
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),
]
