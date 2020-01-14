from allauth.account.auth_backends import AuthenticationBackend
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication


# class EmailOrPhoneModelBackend(object):
# Made this class extend AuthenticationBackend in other to specify a different backend

class EmailOrPhoneModelBackend(object):
    """
    This is a ModelBacked that allows accounts with either a phone or an email address.

    """
    def authenticate(self, request=None, username=None, password=None, **kwargs):

        key = kwargs.get("email", username)
        if '@' in key:
            kwargs = {'email': key}
        else:
            kwargs = {'phone': key}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None

#
# class CsrfExemptSessionAuthentication(SessionAuthentication):
#
#     def enforce_csrf(self, request):
#         return  # To not perform the csrf check previously happening
