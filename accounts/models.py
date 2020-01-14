import os
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.utils import timezone

from core.storage_backends import PublicMediaStorage

MARITAL_STATUS = (("married", "Married"), ("single", "Single"), ("divorced", "Divorced"))
GENDER = (("f", "Female"), ("m", "Male"))


def avatar_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    filename = "{0}{1}".format(int(timezone.now().timestamp()), ext)
    return "user/upload/avatar/{0}".format(filename)


class FbUser(AbstractUser):
    REQUIRED_FIELDS = ["email", "phone", "first_name"]
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    phone = models.CharField(max_length=13, unique=True)
    email = models.EmailField( max_length=254, unique=True, db_index=True)
    username = models.CharField(max_length=500, blank=True, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, storage=PublicMediaStorage(), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designated whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')

    def __str__(self):
        try:
            return "{0} {1}-{2}".format(self.first_name, self.last_name, self.id)
        except:
            return self.email

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name if self.last_name else '')


    def get_avatar(self):
        return self.avatar

    # @property
    # def formated_phone(self):
    #     return "234{}".format(self.phone[1:])

    class Meta:
        verbose_name = "User"




