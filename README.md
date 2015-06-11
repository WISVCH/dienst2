# Dienst2 [![Build Status](https://travis-ci.org/WISVCH/dienst2.svg?branch=master)](https://travis-ci.org/WISVCH/dienst2)
W.I.S.V. 'Christiaan Huygens'
Dienstensysteem v2

## Development installation

1. Install PostgreSQL (e.g. [Postgres.app for OS X](http://postgresapp.com), make sure to add it to `$PATH`
2. Install less and coffee script (`npm install -g coffee-script less`) for the compiling of the assets
3. Install [PyCharm Professional](https://www.jetbrains.com/pycharm/) ([free for students](https://www.jetbrains.com/student/))
4. Open project
5. [Create virtual environment](https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html)
6. Create your own `dienst2/local.py` file (use `local.py.example`)
7. [Install dependencies in virtual environment](https://www.jetbrains.com/pycharm/help/resolving-unsatisfied-dependencies.html)
   * If e.g. psycopg2 won't install, activate virtualenv (`source bin/activate`) and then manually install dependencies (`pip install -r requirements.txt`)
   * If psycopg2 fails during server start, maybe [this](http://stackoverflow.com/questions/28515972/problems-using-psycopg2-on-mac-os-yosemite) solution will work for you.
8. Create database (`createdb dienst2`, `createuser dienst2`)
9. Initialise database [using manage.py](https://www.jetbrains.com/pycharm/help/running-tasks-of-manage-py-utility.html) (`manage.py migrate`)
10. Start server
11. You should be good to go!

**Note: please do not use (a copy of) the production database for local development.**

## Production installation

* Do not forget to install New Relic (`pip install newrelic`)

## API

The API is available at `/ldb/api/v3/`. Authentication is done using a valid session (for in-browser testing) or a token (send an `Authorization: Token <token>` header).

To create an API token:

1. Create a new user through the Django admin interface, please prefix username with `api_`
2. Set password field to `!` in database (e.g. through phpPgAdmin)
3. Assign new API token to new user in Django admin interface

## Update to Django 1.8

To update to Django 1.8

1. `pip install --upgrade south`
2. `pip install django-reversion==1.8`
3. `python manage.py migrate`
4. Make sure you have latest version of dienst2
5. `pip install -r requirements.txt`
6. `python manage.py migrate --fake-initial`

