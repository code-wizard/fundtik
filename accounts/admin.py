from django.contrib import admin
from accounts import models
# Register your models here.

@admin.register(models.FbUser)
class FbUserAdmin(admin.ModelAdmin):
    pass