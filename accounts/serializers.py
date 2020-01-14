# import os
#
# from PIL import Image
# from allauth.account.adapter import get_adapter
# from allauth.account.models import EmailAddress
# from allauth.account.utils import setup_user_email
# from allauth.utils import email_address_exists
# from datetime import datetime, date, timedelta
# from django.utils.translation import  ugettext_lazy as _
# from django.conf import settings
# from django.db import transaction
# from django.utils import timezone
# import time
# from rest_auth.serializers import JWTSerializer, PasswordResetSerializer
# from rest_framework import serializers
# from accounts import models
# from accounts.forms import WsResetPasswordForm
# from accounts.utils import get_last_and_first_from_full_name
#
#
# class WsUserDetailSerailier(serializers.ModelSerializer):
#     is_verified = serializers.SerializerMethodField(read_only=True)
#     is_active = serializers.BooleanField(read_only=True)
#
#     def validate_avatar(self, image):
#
#         if image:
#             img = Image.open(image)
#             fileName, fileExtension = os.path.splitext(image.name)
#             if not fileExtension in ['.jpeg', '.jpeg', '.png', '.jpg', ".JPG", ".PNG", ".JPEG"]:
#                 raise serializers.ValidationError(_("Please use a JPEG or PNG image."))
#             # validate file size
#             if len(image) > 5000000:
#                 raise serializers.ValidationError(_('Image file too large ( maximum 5mb )'))
#             # else:
#             #     raise forms.ValidationError(_("Couldn't read uploaded image"))
#         return image
#
#
#     class Meta:
#         model = models.WsUser
#         fields = ("uuid", "first_name", "last_name", "avatar", "phone", "full_name")
#         # exclude = ("password", "is_staff", "username")
#
#
# class WsSignupSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     full_name = serializers.CharField(max_length=255, required=False)
#     first_name = serializers.CharField(max_length=255, required=False)
#     last_name = serializers.CharField(max_length=255, required=False)
#     phone = serializers.CharField(max_length=11)
#     password1 = serializers.CharField(write_only=True)
#     country = serializers.CharField(max_length=2)
#
#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if email and email_address_exists(email):
#             raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
#         return email
#
#     def validate_phone(self, phone):
#         if get_adapter().validate_unique_phone(phone):
#             raise serializers.ValidationError(_("User with the same phone number already exist."))
#         return phone
#
#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)
#
#     # def validate_unique_phone(self, phone):
#     #     ret = get_user_model().objects.filter(phone__iexact=phone).exists()
#     #     return ret
#     def validate(self, attrs):
#         if not attrs.get("full_name"):
#             attrs["full_name"] = attrs.get("first_name") + " "+attrs.get("last_name") if attrs.get("last_name") else ''
#         return attrs
#
#     def custom_signup(self, request, user):
#         pass
#
#     def get_cleaned_data(self):
#         first_name, last_name = get_last_and_first_from_full_name(self.validated_data.get('full_name', ''))
#         return {
#             'first_name': first_name,
#             'last_name': last_name,
#             'phone': self.validated_data.get('phone', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'email': self.validated_data.get('email', '')
#         }
#
#     def save(self, request, commit=True):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self, commit)
#         self.custom_signup(request, user)
#         # setup_user_email(request, user, [])
#         return user
#
#
# class WsPasswordResetSerializer(serializers.Serializer):
#     username = serializers.CharField()
#
#     password_reset_form_class = WsResetPasswordForm
#
#     def get_email_options(self):
#         """Override this method to change default e-mail options"""
#         return {}
#
#     def validate_username(self, value):
#         # Create PasswordResetForm with the serializer
#         self.reset_form = self.password_reset_form_class(data=self.initial_data)
#         if not self.reset_form.is_valid():
#             raise serializers.ValidationError(self.reset_form.errors)
#
#         return value
#
#     def save(self):
#         request = self.context.get('request')
#         # Set some values to trigger the send_email method.
#         opts = {
#             'use_https': request.is_secure(),
#             'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
#             'request': request,
#         }
#
#         opts.update(self.get_email_options())
#         self.reset_form.save(**opts)
#
