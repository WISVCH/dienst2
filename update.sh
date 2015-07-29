#!/bin/zsh
set -e
if [[ $USER != "www-dienst2" ]]; then 
    echo "This script must be run as www-dienst2!" 
    exit 1
fi
cd /srv/www/dienst2
source .dienst2-env/bin/activate
pip install -U -r requirements.txt
pip install -U newrelic
./manage.py collectstatic --noinput -c
touch dienst2/wsgi.py