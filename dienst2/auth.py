"""
This module provides a Django authentication backend that can be used to

authenticate users using Google Cloud Identity-Aware Proxy (IAP).

Code adapted from
https://github.com/potatolondon/djangae/blob/master/djangae/contrib/googleauth/backends/iap.py
"""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Group

from django.core.exceptions import (
    ImproperlyConfigured,
    SuspiciousOperation,
)
from google.auth.transport import requests
from google.oauth2 import id_token

logger = logging.getLogger(__name__)

_GOOG_AUTHENTICATED_USER_EMAIL_HEADER = "HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL"
_GOOG_AUTHENTICATED_USER_ID_HEADER = "HTTP_X_GOOG_AUTHENTICATED_USER_ID"
_GOOG_JWT_ASSERTION_HEADER = "HTTP_X_GOOG_IAP_JWT_ASSERTION"

User = get_user_model()


class IAPBackend(BaseBackend):
    @classmethod
    def can_authenticate(cls, request):
        return (
            _GOOG_AUTHENTICATED_USER_EMAIL_HEADER in request.META
            and _GOOG_AUTHENTICATED_USER_EMAIL_HEADER in request.META
            and _GOOG_JWT_ASSERTION_HEADER in request.META
        )

    def authenticate(self, request, **kwargs):
        error_partial = "An attacker might have tried to bypass IAP."
        user_id = request.META.get(_GOOG_AUTHENTICATED_USER_ID_HEADER)
        user_email = request.META.get(_GOOG_AUTHENTICATED_USER_EMAIL_HEADER)

        # User not logged in to IAP
        if not user_id or not user_email:
            return

        # All IDs provided should be namespaced
        if ":" not in user_id or ":" not in user_email:
            return

        # Google tokens are namespaced with "auth.google.com:"
        _, user_id = user_id.split(":", 1)
        _, email = user_email.split(":", 1)

        try:
            audience = settings.GOOGLE_IAP_AUDIENCE
        except AttributeError:
            raise ImproperlyConfigured(
                "You must specify a 'GOOGLE_IAP_AUDIENCE' in settings when using"
                " IAPBackend"
            )
        iap_jwt = request.META.get(_GOOG_JWT_ASSERTION_HEADER)

        try:
            signed_user_id, signed_user_email, claims = _validate_iap_jwt(
                iap_jwt, audience
            )
            _, signed_user_id = signed_user_id.split(":", 1)
        except ValueError as e:
            raise SuspiciousOperation(
                "**ERROR: JWT validation error {}**\n{}".format(e, error_partial)
            )

        assert signed_user_id == user_id, (
            f"IAP signed user id does not match {_GOOG_AUTHENTICATED_USER_ID_HEADER}. ",
            error_partial,
        )
        assert signed_user_email == user_email, (
            (
                "IAP signed user email does not match"
                f" {_GOOG_AUTHENTICATED_USER_EMAIL_HEADER}. "
            ),
            error_partial,
        )

        # Verify claims
        if not claims or not verify_claims(claims):
            print(claims)
            raise SuspiciousOperation(
                "**ERROR: User does not have required claims.**\n{}".format(
                    error_partial
                )
            )

        username = email.split("@", 1)[0]

        google_groups = claims["gcip"]["groups"].split(",")
        is_admin = settings.IAP_ADMIN_GROUP in google_groups
        groups = []
        if settings.IAP_USERMAN2_GROUP in google_groups:
            staff_group, created = Group.objects.get_or_create(name="userman2")
            if created:
                staff_group.save()
            groups.append(staff_group)

        # Find a user by their Google Username.
        user = User.objects.filter(username__iexact=username).first()

        if user:
            user.is_staff = is_admin
            user.is_superuser = is_admin
            user.groups.set(groups)

            # If the user doesn't currently have a password, it could
            # mean that this backend has just been enabled on existing
            # data that uses some other authentication system (e.g. the
            # App Engine Users API) - for safety we make sure that an
            # unusable password is set.
            if not user.password:
                user.set_unusable_password()

            # Note we don't update the username, as that may have
            # been overridden by something post-creation
            user.save()
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                is_active=True,
                is_staff=is_admin,
                is_superuser=is_admin,
            )

            user.groups.set(groups)
        return user


def _validate_iap_jwt(iap_jwt, expected_audience):
    """Validate an IAP JWT.

    Args:
      iap_jwt: The contents of the X-Goog-IAP-JWT-Assertion header.
      expected_audience: The Signed Header JWT audience. See
          https://cloud.google.com/iap/docs/signed-headers-howto
          for details on how to get this value.

    Returns:
      (user_id, user_email).
    """

    decoded_jwt = id_token.verify_token(
        iap_jwt,
        requests.Request(),
        audience=expected_audience,
        certs_url="https://www.gstatic.com/iap/verify/public_key",
    )
    return (decoded_jwt["sub"], decoded_jwt["email"], decoded_jwt)


def verify_claims(claims):
    google_groups = claims["gcip"]["groups"].split(",")
    username = "{} ({})".format(claims["email"], claims["sub"])
    has_access = settings.IAP_ACCESS_GROUP in google_groups
    if not has_access:
        logger.warning("%s does not have access (%s)", username, google_groups)
        return False
    return True
