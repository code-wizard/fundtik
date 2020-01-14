from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from accounts import models

#
# @receiver(user_signed_up, sender=models.FbUser)
# def new_sign_up(sender, request, user, **kwargs):
#     country = request.POST.get("country")
#     models.WsUserProfile(
#         country=country,
#         user=user
#     ).save()