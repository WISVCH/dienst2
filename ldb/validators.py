import ldap
from django.core.exceptions import ValidationError

from dienst2.settings import LDAP_HOST, LDAP_USER_DN


def validate_ldap_username(username):
    conn = ldap.initialize(LDAP_HOST)
    dn = LDAP_USER_DN.format(ldap.dn.escape_dn_chars(username))
    try:
        conn.search_s(dn, ldap.SCOPE_ONELEVEL)
    except ldap.NO_SUCH_OBJECT:
        raise ValidationError(
            "User %(username)s does not exist", params={"username": username}
        )


def validate_google_username(username: str, person):
    from ldb.models import Person

    if not username:
        return

    # Check if the username is not an email address
    if "@" in username:
        raise ValidationError(
            "Username %(username)s is not a valid Google username, please use the part before the @",
            params={"username": username},
        )

    # Check if another person has the same username
    if Person.objects.filter(google_username=username).exclude(pk=person.pk).exists():
        raise ValidationError(
            "Google Username %(username)s is already taken",
            params={"username": username},
        )
    
    # Check if another person has an ldap_username that is the same as the google_username
    if Person.objects.filter(ldap_username=username).exclude(pk=person.pk).exists():
        raise ValidationError(
            "Google Username %(username)s is already taken as LDAP username",
            params={"username": username},
        )

    # Check if the person has an ldap_username and if it is the same as the google_username
    if person.ldap_username and person.ldap_username != username:
        raise ValidationError(
            "Google Username %(username)s does not match the LDAP username %(ldap_username)s",
            params={"username": username, "ldap_username": person.ldap_username},
        )

    # TODO: Implement Directory API to check if the username exists in Google Workspace
