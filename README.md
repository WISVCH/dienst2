# Dienst2
W.I.S.V. 'Christiaan Huygens'
Dienstensysteem v2

## Compiling

Run the Makefile after changing any CoffeeScript or Less files.

## Development installation

1. Install PostgreSQL (e.g. [Postgres.app for OS X](http://postgresapp.com), make sure to add it to `$PATH`
2. Install [PyCharm Professional](https://www.jetbrains.com/pycharm/) ([free for students](https://www.jetbrains.com/student/))
3. Open project
4. [Create virtual environment](https://www.jetbrains.com/pycharm/help/creating-virtual-environment.html)
5. Create your own `dienst2/local.py` file (use `local.py.example`)
6. [Install dependencies in virtual environment](https://www.jetbrains.com/pycharm/help/resolving-unsatisfied-dependencies.html)
   * If e.g. psycopg2 won't install, activate virtualenv (`source bin/activate`) and then manually install dependencies (`pip install -r requirements.txt`)
7. Create database (`createdb dienst2`, `createuser dienst2`)
8. Initialise database [using manage.py](https://www.jetbrains.com/pycharm/help/running-tasks-of-manage-py-utility.html) (`manage.py syncdb`, `manage.py migrate`)
9. Start server
10. You should be good to go!

**Note: please do not use (a copy of) the production database for local development.**

[PyCharm also supports CoffeeScript](https://www.jetbrains.com/pycharm/help/transpiling-coffeescript-to-javascript.html): install NodeJS plugin, then `npm install -g coffee-script`. Unfortunately, the file structure will need to be changed if you want to set up a compiler watcher.

## API

To create an API key:

1. Create a new user through the Django admin interface, please prefix username with `api_`
2. Set password field to `!` in database (e.g. through phpPgAdmin)
3. Assign new API key to new user in Django admin interface
