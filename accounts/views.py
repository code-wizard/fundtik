import json

from allauth.account import signals, app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import passthrough_next_redirect_url, perform_login, url_str_to_user_pk, \
    logout_on_password_change, complete_signup, get_next_redirect_url
from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_request_param
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from rest_auth.utils import jwt_encode
from accounts import forms
from allauth.account.views import SignupView, LoginView, ConfirmEmailView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView, PasswordSetView, \
    sensitive_post_parameters_m, PasswordChangeView


# Create your views here.
# from accounts.serializers import WsUserDetailSerailier
from accounts.utils import UiErrorList
# from business.utils import has_business


def activate_email(request):
    return render(request, "accounts/signup_success.html")


class WsSignupView(SignupView):
    template_name = "accounts/signup.html"
    form_class = forms.WsSignupForm
    success_url = reverse_lazy("accounts:activate_email")
    # redirect_field_name = "next"
    # success_url = None

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy("accounts:login_redirect")
        return self.success_url

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request, self.user,
                settings.ACCOUNT_EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'error_class': UiErrorList,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.get_form()
        form = kwargs['form']
        email = self.request.session.get('account_verified_email')
        if email:
            email_keys = ['email']
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("accounts:login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        return {"login_url": login_url,
                "form": form,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value}

signup = WsSignupView.as_view()


class WsConfirmEmailView(ConfirmEmailView):
    template_name = "accounts/email_confirm.html"


confirm_email = WsConfirmEmailView.as_view()


class WsLogoutView(LogoutView):
    redirect_field_name = "next"
    template_name = "accounts/logout.html"

    def render_to_response(self, context, **response_kwargs):
        response = super(WsLogoutView, self).render_to_response(context, **response_kwargs)
        response.delete_cookie("token")
        return response

    def logout(self):
       super(WsLogoutView, self).logout()


logout = WsLogoutView.as_view()


class WsLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = forms.WsLoginForm
    redirect_field_name = "next"
    success_url = reverse_lazy("main:dashboard")
    # success_url = reverse_lazy("guest:home")

    # def render_to_response(self, context, **response_kwargs):
    #     response = super(IbLoginView, self).render_to_response(context, **response_kwargs)
    #     return response

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            # if self.request.user.my_business:
            #     success_url = reverse_lazy("accounts:login_redirect")

            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'error_class': UiErrorList,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.get_form()
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("accounts:signup"),
                                                   self.redirect_field_name)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)
        site = get_current_site(self.request)
        ret = {"signup_url": signup_url,
                    "site": site,
                    "form": kwargs.get("form"),
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value}
        return ret

    # form_class = forms.IbSignupForm

login = WsLoginView.as_view()


def login_redirect(request):
    # success_url = settings.FRONTEND
    # if not has_business(request.user.uuid):
    #     success_url = reverse_lazy("guest:home")
    # response = render(request, "accounts/login_redirect.html", context={"frontend": success_url})
    # response.set_cookie("_u", json.dumps(WsUserDetailSerailier(request.user).data))
    # response.set_cookie("token", jwt_encode(request.user))
    # return response
    return render(request, "accounts/login_redirect.html")


def post_logout_redirect(request):
    response = render(request, "accounts/logout.html")
    response.delete_cookie("token")
    response.delete_cookie("_u")
    return response


class WsPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    # form_class = forms.IbResetPasswordForm
    success_url = reverse_lazy("accounts:reset_password_done")

    def get_context_data(self, **kwargs):
        kwargs["form"] = self.get_form()
        ret = {}
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("accounts:login"),
                                                  self.redirect_field_name)
        # NOTE: For backwards compatibility
        ret['form'] = kwargs.get("form")
        # (end NOTE)
        ret.update({"login_url": login_url})
        return ret

password_reset = WsPasswordResetView.as_view()


class WsPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


password_reset_done = WsPasswordResetDoneView.as_view()


class WsPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "accounts/password_reset_from_key.html"
    success_url = reverse_lazy("accounts:reset_password_from_key_done")

    def get_context_data(self, **kwargs):
        ret = {}
        ret["form"] = self.get_form()
        ret['action_url'] = reverse(
            'accounts:reset_password_from_key',
            kwargs={'uidb36': self.kwargs['uidb36'],
                    'key': self.kwargs['key']})
        return ret

    def form_valid(self, form):
        form.save()
        get_adapter(self.request).add_message(
            self.request,
            messages.SUCCESS,
            'accounts/messages/password_changed.txt')
        signals.password_reset.send(sender=self.reset_user.__class__,
                                    request=self.request,
                                    user=self.reset_user)

        if app_settings.LOGIN_ON_PASSWORD_RESET:
            return perform_login(
                self.request, self.reset_user,
                email_verification=app_settings.EMAIL_VERIFICATION)
        return super(WsPasswordResetFromKeyView, self).form_valid(form)


password_reset_from_key = WsPasswordResetFromKeyView.as_view()


class WsPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = "accounts/password_reset_from_key_done.html"

password_reset_from_key_done = WsPasswordResetFromKeyDoneView.as_view()


class WsPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:change_password")

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse('accounts:set_password'))
        return super(PasswordChangeView, self).render_to_response(
            context, **response_kwargs)

    def form_valid(self, form):
        form.save()
        logout_on_password_change(self.request, form.user)
        get_adapter(self.request).add_message(
            self.request,
            messages.SUCCESS,
            'accounts/messages/password_changed.txt')
        signals.password_changed.send(sender=self.request.user.__class__,
                                      request=self.request,
                                      user=self.request.user)
        return super(PasswordChangeView, self).form_valid(form)

password_change = login_required(WsPasswordChangeView.as_view())


def staff(request):
    return render(request, "accounts/staff.html")
