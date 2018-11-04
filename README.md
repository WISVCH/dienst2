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
   * On macOS, install python-ldap using:
     `pip install -U python-ldap --global-option=build_ext --global-option="-I$(xcrun --show-sdk-path)/usr/include/sasl"`
6. Install dependencies using Yarn (`yarn install`; first install [Node.js][nodejs] and [Yarn][yarn] if you haven't already)
7. Create PostgreSQL database (`createdb dienst2`; `createuser dienst2`)
8. Edit the `dienst2/local.py` file to set up your database
9. Initialise database [using manage.py](https://www.jetbrains.com/pycharm/help/running-tasks-of-manage-py-utility.html) (`./manage.py migrate`)
10. Initialize user auth, either:
    * Connect to [CH VPN](https://ch.tudelft.nl/vpn/) and log in with a CH account that is in the `dienst2` group. Or,
    * Connect to your own LDAP server (Override `AUTH_LDAP*` values in your `dienst2/local.py`). Or,
    * Create local superuser (`./manage.py createsuperuser`)
11. Start server (`./manage.py runserver`) and go to http://localhost:8000

**Note: please do not use (a copy of) the production database for local development.**

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
