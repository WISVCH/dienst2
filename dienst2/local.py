# Example for development purposes only!

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dienst2',
        'USER': 'dienst2',
        'PASSWORD': '',
        'HOST': 'postgres',
        'PORT': '',
        'CONN_MAX_AGE': 10800,
        'ATOMIC_REQUESTS': True
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGEME'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = '/tmp/dienst2-static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
    },
}
