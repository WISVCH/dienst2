import os
from email.utils import getaddresses

import environ

env = environ.Env()

# Django settings for dienst2 project.

DEBUG = env.bool("DEBUG", default=False)

ADMINS = getaddresses([env("DJANGO_ADMINS", default="")])
MANAGERS = ADMINS

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = env.list("INTERNAL_IPS", default="")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATABASES = {"default": env.db()}

CACHES = {"default": env.cache()}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHES = env(
    "CACHES",
    default={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SECRET_KEY = env("SECRET_KEY")
SESSION_ENGINE = env("SESSION_ENGINE", default="django.contrib.sessions.backends.db")
EMAIL_HOST = env("EMAIL_HOST", default="")
LDAP_HOST = "ldaps://ank.chnet"
LDAP_USER_DN = "uid={},ou=People,dc=ank,dc=chnet"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Europe/Amsterdam"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "nl-NL"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))

LOCALE_PATHS = (os.path.join(SITE_ROOT, "locale"),)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ""

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../static/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ""

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "dienst2.middleware.RequireLoginMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

ROOT_URLCONF = "dienst2.urls"

LOGIN_REDIRECT_URL = "/"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "dienst2.wsgi.application"

INSTALLED_APPS = (
    "bootstrap4",
    "dienst2",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "reversion",
    "reversion_compare",
    "mozilla_django_oidc",
    "import_export",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django_select2",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "debug_toolbar",
    "ddtrace.contrib.django",
    "ldb",
    "post",
)

OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")
OIDC_RP_SCOPES = "openid profile ldap email"
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://connect.ch.tudelft.nl/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://connect.ch.tudelft.nl/token"
OIDC_OP_USER_ENDPOINT = "https://connect.ch.tudelft.nl/userinfo"
OIDC_OP_JWKS_ENDPOINT = "https://connect.ch.tudelft.nl/jwk"
OIDC_OP_LOGOUT_URL_METHOD = "dienst2.auth.provider_logout"
OIDC_LDAP_ACCESS_GROUP = env("OIDC_LDAP_ACCESS_GROUP", default="dienst2")
OIDC_LDAP_ADMIN_GROUP = env("OIDC_LDAP_ADMIN_GROUP", default="dienst2-admin")
OIDC_LDAP_USERMAN2_GROUP = env("OIDC_LDAP_USERMAN2_GROUP", default="staff")
LOGIN_REDIRECT_URL_FAILURE = "/forbidden"

IMPORT_EXPORT_USE_TRANSACTIONS = True

AUTHENTICATION_BACKENDS = ("dienst2.auth.CHConnect",)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s.\
                %(funcName)s:%(lineno)s %(message)s"
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "loggers": {
        "dienst2": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "ldb": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "post": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.request": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.security": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "health-check": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "health_check": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "rest_framework": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}

BOOTSTRAP4 = {
    "horizontal_label_class": "col-md-4",
    "horizontal_field_class": "col-md-8",
}
