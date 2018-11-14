#!/bin/bash
set -e

if [ "$1" = 'dev' ]; then
    yarn install
    until nc -z postgres 5432 > /dev/null 2>&1; do
      echo "Waiting for postgres..."
      sleep 5
    done
    ./manage.py migrate --noinput
    exec python -Wall ./manage.py runserver 0.0.0.0:8000
fi

exec "$@"
