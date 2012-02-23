# Django settings for dienst2 project.
import os
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-NL'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ldb.middleware.RequireLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'dienst2.urls'

LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'haystack',
    'djangorestframework',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'ldb'
)

AUTH_LDAP_SERVER_URI = "ldaps://frans.chnet/"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=ank,dc=chnet", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc=ank,dc=chnet",
    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_REQUIRE_GROUP = "cn=dienst2,ou=Overig,ou=Group,dc=ank,dc=chnet"

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=dienst2,ou=Overig,ou=Group,dc=ank,dc=chnet",
    # "is_active": "cn=bestuur,ou=Besturen,ou=Group,dc=ank,dc=chnet",
    "is_staff": "cn=secretaris,ou=Group,dc=ank,dc=chnet",
    "is_superuser": "cn=secretaris,ou=Group,dc=ank,dc=chnet"
}

AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
    "is_awesome": "cn=bestuur54,ou=Besturen,ou=Group,dc=ank,dc=chnet",
}

AUTH_LDAP_MIRROR_GROUPS = True

# FIXME: Do not use for deployment!
AUTH_LDAP_GLOBAL_OPTIONS = { ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER }

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

HAYSTACK_SITECONF = 'ldb.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
# HAYSTACK_INCLUDE_SPELLING = True

from local import *