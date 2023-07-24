from django.contrib.auth.management.commands import createsuperuser
from django.contrib.auth.models import User
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = "Crate a superuser, and allow password to be provided"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Specifies the password for the superuser.",
        )

    def handle(self, *args, **options):
        password = options["password"]
        username = options["username"]
        database = options["database"]
        options["interactive"] = False

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists.")
            return

        super().handle(*args, **options)

        if password:
            user = self.UserModel._default_manager.db_manager(database).get(
                username=username
            )
            user.set_password(password)
            user.save()
