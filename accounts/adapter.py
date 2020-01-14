from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username, user_field, setup_user_email
from allauth.utils import build_absolute_uri
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend

from accounts.utils import get_last_and_first_from_full_name


class WsAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "accounts:confirm_email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url)
        return ret

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        # from .utils import user_username, user_email, user_field

        data = form.cleaned_data
        full_name =  data.get('full_name')
        if full_name:
            first_name, last_name = get_last_and_first_from_full_name(full_name)
        else:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
        phone = data.get('phone')
        email = data.get('email')
        # username = data.get('username')
        username = email
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        if phone:
            user_field(user, "phone", phone)
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        setup_user_email(request, user, [])
        return user

    def validate_unique_phone(self, phone):
        ret = get_user_model().objects.filter(phone__iexact=phone).exists()
        return ret
