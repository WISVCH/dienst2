# Dienst2
W.I.S.V. 'Christiaan Huygens'
Dienstensysteem v2

# Development installation

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

Note: please do not use (a copy of) the production database for local development.
