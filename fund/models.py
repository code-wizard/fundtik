import os

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.utils import timezone

FbUser = get_user_model()


def doc_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = "{0}{1}".format(int(timezone.now().timestamp()), ext)
    return "funding/upload/{0}".format(filename)


class FbFunding(models.Model):
    agency = models.CharField(max_length=255)
    fund_name = models.CharField(max_length=255)
    web_link = models.CharField(max_length=255, null=True)
    opening_date = models.DateField()
    closing_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    occurrence = models.CharField(max_length=255)
    occurrence_no = models.PositiveIntegerField(null=True)
    amount = models.FloatField(null=True)
    qualifiers = models.TextField(null=True)
    key_contacts = models.TextField(null=True)
    created_by = models.ForeignKey(FbUser, related_name="created_funds", on_delete=models.CASCADE, null=True)

    requirements = models.TextField(null=True)
    file = models.FileField(upload_to=doc_upload_path, null=True)
    document_id = models.CharField(max_length=255, null=True)
    categories = ArrayField(base_field=models.CharField(max_length=255))






