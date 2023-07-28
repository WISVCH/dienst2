# Dienst2

W.I.S.V. 'Christiaan Huygens'
Dienstensysteem v2

## Development

### Using GitHub Codespaces or VS Code

This repository has [Development Containers][devcontainers] configuration files, making it easy to use [GitHub Codespaces][codespaces] to develop remotely or [Visual Studio Code Dev Containers][vscode] to develop locally. Simply open this repository using one of these editors and use the 'Run' menu to start the Dienst2 application server.

[devcontainers]: https://containers.dev
[codespaces]:    https://docs.github.com/en/codespaces
[vscode]:        https://code.visualstudio.com/docs/devcontainers/containers


For Visual Studio Code:
1. Run 'Dev Containers: Open Folder in Container' from the Command Palette (Ctrl+Shift+P) to open the repository in a container.
2. Wait for the container to install.
3. Start the server by running 'Run: Start Debugging' from the menu (F5).

### Using Docker

Build and run the development Docker image using [Docker Compose](https://docs.docker.com/compose/install/): `docker-compose up` and go to http://localhost:8000

### Without Docker

1. Install PostgreSQL (e.g. [Postgres.app for macOS](https://postgresapp.com), make sure to add it to `$PATH`)
2. Install [PyCharm Professional](https://www.jetbrains.com/pycharm/) ([free for students](https://www.jetbrains.com/student/))
3. Open project
4. [Create virtual environment](https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html)
5. [Install dependencies in virtual environment](https://www.jetbrains.com/pycharm/help/resolving-unsatisfied-dependencies.html)
6. Install dependencies using Yarn (`yarn install`; first install [Node.js][nodejs] and [Yarn][yarn] if you haven't already)
7. Run pre-commit install (`pre-commit install`)
8. Create PostgreSQL database (`createdb dienst2`; `createuser dienst2`)
9. Edit the `dienst2/local.py` file to set up your database
10. Initialise database [using manage.py](https://www.jetbrains.com/pycharm/help/running-tasks-of-manage-py-utility.html) (`./manage.py migrate`)
11. Start server (`./manage.py runserver`) and go to http://localhost:8000

**Note: please do not use (a copy of) the production database for local development.**

## Translation files

We use django-admin `make-messages` for localisation.
The translations are generated in `.po` files, such as [this django.po file](dienst2/locale/nl/LC_MESSAGES/django.po).
Please beware that these files should not be edited by hand, except for the translations themselves.
For an example of translations in a file, please check [this file](ldb/templates/ldb/person_confirm_delete.html).

### With Docker

If you run your development environment using docker, the generation of the translation files is done using the following command:
`docker-compose run django python manage.py makemessages -l nl -i venv --no-location` at the root of the project.
In this case we are generating the Dutch (nl) translation files.

To compile the messages run `docker-compose run django python manage.py compilemessages -l nl`

## Production deployment

The `master` branch should be automatically deployed to the CH Kubernetes cluster through GitHub Actions and Flux.

## Google Serivce Account
Dienst2 requires a Google Service account to access Group and Member data via the directory API. A Google Serivce Account can be created in the [Google Cloud Console](https://console.cloud.google.com/apis/credentials). The service account should be a "Domain-wide Delegation" account with the following scopes:

- https://www.googleapis.com/auth/admin.directory.group.readonly
- https://www.googleapis.com/auth/admin.directory.group.member.readonly

The scopes can be defined in Google Admin Console -> Security -> API controls -> Domain-wide delegation.

After creating the service account, a JSON key file should be downloaded and stored in `/google-service-account.json` on the server.

It is also required to set the subject of the service account as an environment variable `GOOGLE_SERVICE_ACCOUNT_DELEGATED_USER`. Service accounts are used to represent non-human entities, but some APIs require a human user to be impersonated.

**I do not know to what value this should be set in production, but for development, every email address of someone from "beheer" should work.**

## API

The API is available at `/ldb/api/v3/`. Authentication is done using a valid session (for in-browser testing) or a token (send an `Authorization: Token <token>` header).

To create an API token:

1. Create a new user through the Django admin interface, please prefix username with `api_`
2. Set password field to `!` in database (e.g. through phpPgAdmin)
3. Assign new API token to new user in Django admin interface

[nodejs]: https://nodejs.org/ "Node.js"
[yarn]:   https://yarnpkg.com/lang/en/docs/install "Yarn"


## IAP
Testing the IAP in a local environment is not straightforward. 3 headers are required for the IAP. Headers for development can be retrieved from the following page: https://wisvch.ew.r.appspot.com/resource.

```sh
x-goog-authenticated-user-email=securetoken.google.com/wisvch:[USERNAME]@ch.tudelft.nl
x-goog-authenticated-user-id=securetoken.google.com/wisvch:[SUB]
x-goog-iap-jwt-assertion=[JWT]
```

You can set the headers using `Postman` or using this [Chrome Plugin](https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj)

The page https://wisvch.ew.r.appspot.com/resource uses `GOOGLE_IAP_AUDIENCE=/projects/966138216790/apps/wisvch` audience.
