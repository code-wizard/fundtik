from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str, user_username, perform_login, filter_users_by_email, \
    setup_user_email
from allauth.utils import set_form_field_order, build_absolute_uri
from django import forms
from allauth.account.forms import LoginForm, SignupForm, PasswordField, ResetPasswordForm, default_token_generator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.forms import TextInput, CharField
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import  ugettext_lazy as _

from accounts.utils import filter_users_by_email_or_phone


class WsLoginForm(LoginForm):
    error_messages = {
        'account_inactive':
            _("This account is currently inactive."),

        'email_password_mismatch':
            _("The e-mail address and/or password you specified are not correct."),

        'username_password_mismatch':
            _("Invalid login details. Please try again."),
    }
    password = PasswordField(label=_("Password"))

    user = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(WsLoginForm, self).__init__(*args, **kwargs)
        # del self.fields["remember"]
        login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Email'),
                                              'autofocus': 'autofocus'})
        login_field = forms.CharField(label="Login",
                                      widget=login_widget)
        self.fields["login"] = login_field

        set_form_field_order(self, ["login", "password", "remember"])

    def login(self, request, redirect_url=None):
        ret = perform_login(request, self.user,
                            email_verification=app_settings.EMAIL_VERIFICATION,
                            redirect_url=redirect_url)
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


class WsSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(WsSignupForm, self).__init__(*args, **kwargs)

        self.fields["phone"] = CharField(
            widget=TextInput(attrs={
                "type": "tel",
                "maxlength": "11",
                "placeholder": _("Phone Number")
            }))
        self.fields["email"] = CharField(
            widget=TextInput()
        )
        self.fields["full_name"] = CharField(widget=TextInput(attrs={
            "maxlength": 50,
            "placeholder": _("Full Name"),
        }))
        self.fields["country"] = CharField(widget=TextInput(
            attrs={
                "value":"NG"
            }
        ), required=False)

    def clean_country(self):
        country = "NG" if not self.cleaned_data["country"] else self.cleaned_data["country"]
        if not country:
            raise forms.ValidationError(_("Please select country"))
        return  country

    def clean_phone(self):
        value = self.cleaned_data['phone']
        if get_adapter().validate_unique_phone(value):
            raise forms.ValidationError(_("User with the same phone number already exist."))
        return value

    def clean_email(self):
        value = self.cleaned_data["email"]
        return get_adapter().validate_unique_email(value)


    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)

        return user
    # def save(self, request):
    #     user = super(WsSignupForm, self).save(request)
    #     return user


class WsResetPasswordForm(forms.Form):

    email = forms.CharField(
        label=_("Email"),
        required=True,
        widget=forms.TextInput(attrs={
            "type": "text",
            "size": "30",
            "placeholder": _("Email"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data["username"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        # self.users = filter_users_by_email_or_phone(email)
        if not self.email:
            raise forms.ValidationError(_("The e-mail address is not assigned to any user account"))
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse("accounts:reset_password_from_key",
                           kwargs=dict(uidb36=user_pk_to_url_str(user),
                                       key=temp_key))
            url = build_absolute_uri(
                request, path)

            context = {"current_site": current_site,
                       "user": user,
                       "password_reset_url": url,
                       "request": request}

            # if app_settings.AUTHENTICATION_METHOD \
            #         != AuthenticationMethod.EMAIL:
            # context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'accounts/email/password_reset_key',
                user.email,
                context)
        return self.cleaned_data["email"]

