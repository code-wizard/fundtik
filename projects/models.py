from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
import os

from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.utils import timezone

from fund.models import FbFunding

FbUser = get_user_model()

def doc_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = "{0}{1}".format(int(timezone.now().timestamp()), ext)
    return "projects/upload/{0}".format(filename)


class FbProjects(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    funding = models.ManyToManyField(FbFunding, related_name="project_funding")
    created_by = models.ForeignKey(FbUser, related_name="created_projects", on_delete=models.CASCADE)
    description = models.TextField()
    budget = models.FloatField(null=True)
    file = models.FileField(upload_to=doc_upload_path, null=True, blank=True)
    # status = models.CharField(max_length=255, default="Not Submitted")
    # categories = ArrayField(base_field=models.CharField(max_length=255))


class FbMileStones(models.Model):
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(FbFunding, related_name="project_milestones", on_delete=models.CASCADE)
    created_by = models.ForeignKey(FbUser, related_name="created_milestone", on_delete=models.CASCADE)
    assignee = models.ForeignKey(FbUser, related_name="assigned_milestones", on_delete=models.CASCADE)
    description = models.TextField()
    reminder = models.PositiveIntegerField()
    file = models.FileField(upload_to=doc_upload_path, null=True, blank=True)





