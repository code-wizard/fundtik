from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
import os
from django.contrib.postgres.fields import ArrayField

from fund.models import FbFunding
from projects.models import FbProjects

FbUser = get_user_model()
APPLICATION_STATUS = (("not submitted", "Not Submitted"), )


class FbApplication(models.Model):
    project = models.ForeignKey(FbProjects, related_name="project_applications", on_delete=models.CASCADE)
    funding = models.ForeignKey(FbFunding, related_name="funding_applications", on_delete=models.CASCADE)
    request = models.ForeignKey(FbUser, related_name="my_approve_requests", on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default="not submitted", null=True,
                              choices=APPLICATION_STATUS, blank=True)
    created_by = models.ForeignKey(FbUser, related_name="created_application", on_delete=models.CASCADE)






