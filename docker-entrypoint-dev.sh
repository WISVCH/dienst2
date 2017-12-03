#!/bin/bash
set -e

if [ "$1" = 'dev' ]; then
    bower --allow-root install
    ./manage.py compress
    until nc -z postgres 5432 > /dev/null 2>&1; do
      echo "Waiting for postgres..."
      sleep 5
    done
    ./manage.py migrate --noinput
    ./manage.py createdevsuperuser --username admin --password admin --email admin@example.com
    echo Running server on http://localhost:8000, log in with admin / admin
    exec ./manage.py runserver 0.0.0.0:8000
fi

exec "$@"
