from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from accounts import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from accounts import api

app_name = "accounts"

# bank = DefaultRouter()
# bank.register(r"", api.IbLinkedBankAccountViewset, "banks")

urlpatterns = [

    path("signup/", views.signup, name="signup"),
    path("staff/", views.staff, name="staff"),
    path("signup/activate-email", views.activate_email, name="activate_email"),
    path("login-redirect/", views.login_redirect, name="login_redirect"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("post-logout/", views.post_logout_redirect, name="post-logout"),
    path("password/change/", views.password_change, name="change_password"),
    # path("password/set/", views.password_set, name="set_password"),
    path("password/reset/", views.password_reset, name="reset_password"),
    path("password/reset/done/", views.password_reset_done, name="reset_password_done"),
    path("password/reset/key/done/", views.password_reset_from_key_done, name="reset_password_from_key_done"),
    # path("password/reset/key/<uidb36>-<key>/", views.password_reset_from_key, name="reset_password_from_key"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key,
            name="reset_password_from_key"),
    path("confirm-email/<key>/", views.confirm_email, name="confirm_email"),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/signup/', include('rest_auth.registration.urls')),
    path('jwt/api-token-auth/', obtain_jwt_token),
    path('jwt/api-token-refresh/', refresh_jwt_token),
    path('jwt/api-token-verify/', verify_jwt_token),
    path("resend-confirm-email/", api.WsResendActivationEmailAPIView.as_view(), name="resend_account_confirm"),

    # path('api/v1/get-profile/', api.IbGetProfileAPIView.as_view()),
    # path('api/v1/edit-profile/', api.IbGetProfileAPIView.as_view()),
    # # path('api/v1/search-users', api.IbUserSearchAPIView.as_view()),

    # path("", include('allauth.urls')),
]