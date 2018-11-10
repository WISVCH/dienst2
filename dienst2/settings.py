import os
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

# Django settings for dienst2 project.

DEBUG = env('DEBUG')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-NL'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]

MIDDLEWARE = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'mozilla_django_oidc.middleware.SessionRefresh',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dienst2.middleware.RequireLoginMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'dienst2.urls'

LOGIN_REDIRECT_URL = '/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dienst2.wsgi.application'

INSTALLED_APPS = (
    'dienst2',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'reversion',
    'reversion_compare',
    'mozilla_django_oidc',
    'haystack',
    'tastypie',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'debug_toolbar',
    'ddtrace.contrib.django',

    'bootstrap3',

    'ldb',
    'kas',
    'post',
)

OIDC_RP_CLIENT_ID = env('OIDC_RP_CLIENT_ID', default='dienst2-dev')
OIDC_RP_CLIENT_SECRET = env('OIDC_RP_CLIENT_SECRET', default='D6EFUL5Nvod2I_yYcqYhlpJr_EHoTaV4l7hp3GzUaYMtjpTPjuwUSK0g_HxG2EQjYZrAvY2yGvmZ4_tkr3Mzbg')
OIDC_RP_SCOPES = 'openid profile ldap'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://connect.ch.tudelft.nl/authorize'
OIDC_OP_TOKEN_ENDPOINT = 'https://connect.ch.tudelft.nl/token'
OIDC_OP_USER_ENDPOINT = 'https://connect.ch.tudelft.nl/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://connect.ch.tudelft.nl/jwk'
OIDC_OP_LOGOUT_URL_METHOD = 'dienst2.auth.provider_logout'
OIDC_LDAP_ACCESS_GROUP = env('OIDC_LDAP_ACCESS_GROUP', default='dienst2')
OIDC_LDAP_ADMIN_GROUP = env('OIDC_LDAP_ADMIN_GROUP', default='dienst2-admin')
OIDC_LDAP_USERMAN2_GROUP = env('OIDC_LDAP_USERMAN2_GROUP', default='staff')
LOGIN_REDIRECT_URL_FAILURE = '/forbidden'

AUTHENTICATION_BACKENDS = (
    'dienst2.auth.CHConnect',
)

DATADOG_TRACE = {
    'DEFAULT_SERVICE': 'dienst2',
    'DEFAULT_DATABASE_PREFIX': 'dienst2',
    'DISTRIBUTED_TRACING': True,
    'TAGS': {'env': 'production'},
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
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
    },
}

BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-4',
    'horizontal_field_class': 'col-md-8',
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

from .local import *
