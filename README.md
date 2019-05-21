# Dienst2 [![Build Status](https://travis-ci.org/WISVCH/dienst2.svg?branch=master)](https://travis-ci.org/WISVCH/dienst2) [![Requirements Status](https://requires.io/github/WISVCH/dienst2/requirements.svg?branch=master)](https://requires.io/github/WISVCH/dienst2/requirements/?branch=master)
W.I.S.V. 'Christiaan Huygens'
Dienstensysteem v2

## Development installation

### With Docker

1. Build and run the development Docker image using [Docker Compose](https://docs.docker.com/compose/install/): `docker-compose up` and go to http://localhost:8000

### Without Docker

1. Install PostgreSQL (e.g. [Postgres.app for OS X](http://postgresapp.com), make sure to add it to `$PATH`
2. Install [PyCharm Professional](https://www.jetbrains.com/pycharm/) ([free for students](https://www.jetbrains.com/student/))
3. Open project
4. [Create virtual environment](https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html)
5. [Install dependencies in virtual environment](https://www.jetbrains.com/pycharm/help/resolving-unsatisfied-dependencies.html)
   * If e.g. psycopg2 won't install, activate virtualenv (`source bin/activate`) and then manually install dependencies (`pip install -r requirements.txt`)
   * If psycopg2 fails during server start, maybe [this](http://stackoverflow.com/questions/28515972/problems-using-psycopg2-on-mac-os-yosemite) solution will work for you.
6. Install dependencies using Yarn (`yarn install`; first install [Node.js][nodejs] and [Yarn][yarn] if you haven't already)
7. Create PostgreSQL database (`createdb dienst2`; `createuser dienst2`)
8. Edit the `dienst2/local.py` file to set up your database
9. Initialise database [using manage.py](https://www.jetbrains.com/pycharm/help/running-tasks-of-manage-py-utility.html) (`./manage.py migrate`)
10. Start server (`./manage.py runserver`) and go to http://localhost:8000

**Note: please do not use (a copy of) the production database for local development.**

## Translation files

We use django-admin `make-messages` for localisation. 
The translations are generated in `.po` files, such as [this django.po file](dienst2/locale/nl/LC_MESSAGES/django.po).
Please beware that these files should not be edited by hand, except for the translations themselves.
For an example of translations in a file, please check [this file](ldb/templates/ldb/person_confirm_delete.html).

### With docker
If you run your development environment using docker, the generation of the translation files is done using the following command: `docker-compose run django python manage.py makemessages -l nl -i venv` at the root of the project.
In this case we are generating the Dutch (nl) translation files.

To compile the messages run `docker-compose run django python manage.py compilemessages -l nl`

## Production deployment

Keel automatically deploys the `master` branch to the CH Kubernetes cluster.

## API

The API is available at `/ldb/api/v3/`. Authentication is done using a valid session (for in-browser testing) or a token (send an `Authorization: Token <token>` header).

To create an API token:

1. Create a new user through the Django admin interface, please prefix username with `api_`
2. Set password field to `!` in database (e.g. through phpPgAdmin)
3. Assign new API token to new user in Django admin interface

[nodejs]: https://nodejs.org/ "Node.js"
[yarn]:   https://yarnpkg.com/lang/en/docs/install "Yarn"
