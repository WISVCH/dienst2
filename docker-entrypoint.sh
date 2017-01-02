#!/bin/bash
set -e

if [ "$1" = 'gunicorn' ]; then
    ./manage.py migrate --noinput
    ./manage.py collectstatic --noinput -c
    exec "$@" -b 0.0.0.0 dienst2.wsgi
fi

exec "$@"
