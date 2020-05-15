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
