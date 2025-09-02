#!/bin/bash
set -e

if [ "$1" = 'dev' ]; then
    ./manage.py migrate --noinput
    exec python -Wall ./manage.py runserver 0.0.0.0:8000
fi

exec "$@"
