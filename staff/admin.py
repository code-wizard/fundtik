from django.contrib import admin
from .models import Staff

# Register your models here.

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'position', 'created_at')
    list_filter = ('position', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)
