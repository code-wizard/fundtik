import datetime
import os

from Crypto.PublicKey import RSA
from PIL import Image
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import perform_login, user_email, cleanup_email_addresses
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from allauth.account import signals
from django.forms.utils import ErrorList
from rest_framework import serializers
import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm


def get_last_and_first_from_full_name(full_name):
    full_name = full_name.split(" ")
    first_name = full_name[0] if len(full_name) else  None
    last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ""
    return first_name, last_name


def filter_users_by_email_or_phone(email_phone):
    """Return list of users by email address or phone no

    Typically one, at most just a few in length.  First we look through
    EmailAddress table, than customisable User model table. Add results
    together avoiding SQL joins and deduplicate.
    """
    User = get_user_model()
    users = User.objects.filter(Q(email__iexact=email_phone)|Q(phone__iexact=email_phone))
    # users += list(User.objects.filter(**q_dict))
    return list(set(users))


class UiErrorList(ErrorList):

     def __str__(self):
         return self.as_divs()

     def as_divs(self):
         if not self: return ''
         return '<ul class="parsley-errors-list filled">%s</ul>' % \
                ''.join(['<li class="parsley-required">%s</li>' % e for e in self])


def validate_image_file(image, size):
    img = Image.open(image)
    fileName, fileExtension = os.path.splitext(image.name)
    if not fileExtension in ['.jpeg', '.jpeg', '.png', '.jpg']:
        raise serializers.ValidationError(_("Please use a JPEG or PNG image."))
    # validate file size
    if len(image) > ( size ):
        raise serializers.ValidationError(_('Image file too large ( maximum 5mb )') )


def complete_signup(request, user, email_verification, success_url=None,
                    signal_kwargs=None):
    if signal_kwargs is None:
        signal_kwargs = {}
    signals.user_signed_up.send(sender=user.__class__,
                                request=request,
                                user=user,
                                **signal_kwargs)
    return perform_login(request, user,
                         email_verification=email_verification,
                         signup=True,
                         redirect_url=success_url,
                         signal_kwargs=signal_kwargs)


def setup_user_email(request, user, addresses):
    """
    Creates proper EmailAddress for the user that was just signed
    up. Only sets up, doesn't do any other handling such as sending
    out email confirmation mails etc.
    """
    # from .models import EmailAddress

    assert not EmailAddress.objects.filter(user=user).exists()
    priority_addresses = []
    # Is there a stashed e-mail?
    adapter = get_adapter(request)
    # stashed_email = adapter.unstash_verified_email(request)
    # if stashed_email:
    #     priority_addresses.append(EmailAddress(user=user,
    #                                            email=stashed_email,
    #                                            primary=True,
    #                                            verified=True))
    email = user_email(user)
    if email:
        priority_addresses.append(EmailAddress(user=user,
                                               email=email,
                                               primary=True,
                                               verified=False))
    addresses, primary = cleanup_email_addresses(
        request,
        priority_addresses + addresses)
    for a in addresses:
        a.user = user
        a.save()
    EmailAddress.objects.fill_cache_for_user(user, addresses)
    if (primary and email and email.lower() != primary.email.lower()):
        user_email(user, primary.email)
        user.save()
    return primary


def generate_jwt(user, document, **kwargs):
    # jwt.unregister_algorithm('RS256')
    permissions = ["read-document", "write"]
    # jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
    key = open("./jwtRS256.key", "rb")
    # rsa_key = RSA.importKey(key.read(), passphrase="secret")
    s = key.read()
    rsa_key = load_pem_private_key(s, password=b'fundkit-passphrase', backend=default_backend())
    encoded_jwt = jwt.encode({"document_id": document,
                              # "user_id": str(user.uuid),
                              "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
                              "permissions": permissions}, rsa_key, algorithm="RS256")
    return str(encoded_jwt, "utf-8")