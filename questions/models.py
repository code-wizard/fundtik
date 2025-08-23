from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
import os


# Create your models here.
from django.utils import timezone

FbUser = get_user_model()


class FbQuestions(models.Model):
    title = models.CharField(max_length=255)
    answer = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(FbUser, related_name="created_questions", on_delete=models.CASCADE)
    life_cycle = models.PositiveIntegerField()
    # Store tags as a comma-separated string (SQLite compatible)
    tag = models.TextField(null=True, blank=True, help_text="Comma-separated tags")





