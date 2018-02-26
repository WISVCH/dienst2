#!/bin/bash
set -e

if [ "$1" = 'gunicorn' ]; then
    ./manage.py migrate --noinput
    until curl -sf http://localhost:9200 > /dev/null; do
        echo 'Waiting for Elasticsearch'
        sleep 1
    done
    ./manage.py rebuild_index --noinput &
    export DATADOG_SERVICE_NAME=dienst2
    exec ddtrace-run "$@" -b 0.0.0.0 dienst2.wsgi
fi

exec "$@"
