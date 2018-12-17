import logging

from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from dienst2 import settings

logger = logging.getLogger(__name__)


class CHConnect(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super(CHConnect, self).verify_claims(claims)
        username = "%s (%s)" % (claims.get('sub'), claims.get('ldap_username'))
        if not verified:
            logger.warning("Could not verify claims for %s", username)
        ldap_groups = claims.get('ldap_groups', [])
        has_access = settings.OIDC_LDAP_ACCESS_GROUP in ldap_groups
        if not has_access:
            logger.warning("%s does not have access (%s)", username, ldap_groups)
        if verified and has_access:
            logger.info("%s successfully logged in", username)
        return verified and has_access

    def filter_users_by_claims(self, claims):
        username = self.get_username(claims)
        if not username:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username=username)

    def get_username(self, claims):
        # We use ldap_username instead of sub for backwards compatibility
        return claims.get('ldap_username')

    def create_user(self, claims):
        user = super(CHConnect, self).create_user(claims)

        username = self.get_username(claims)
        if not username:
            return self.UserModel.objects.none()

        self.set_attributes(user, claims)

        return user

    def update_user(self, user, claims):
        self.set_attributes(user, claims)

        user.save()

        return user

    def set_attributes(self, user, claims):
        ldap_groups = claims.get('ldap_groups', [])

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.email = claims.get('email', '')

        user.is_active = True
        is_admin = settings.OIDC_LDAP_ADMIN_GROUP in ldap_groups
        user.is_staff = is_admin
        user.is_superuser = is_admin

        user.set_unusable_password()

        groups = []
        if settings.OIDC_LDAP_USERMAN2_GROUP in ldap_groups:
            staff_group, created = Group.objects.get_or_create(name='userman2')
            if created:
                staff_group.save()
            groups.append(staff_group)
        user.groups.set(groups)


def provider_logout(request):
    return 'https://connect.ch.tudelft.nl/endsession'
