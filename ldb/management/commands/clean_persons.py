from __future__ import unicode_literals

from sys import stderr

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from ldb.models import Alumnus, Member, Person, Student

BASE_URL = "https://dienst2.ch.tudelft.nl/ldb/people/"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--no-persons",
            action="store_false",
            dest="clean-persons",
            default=True,
            help="Do not run full_clean for persons",
        )
        parser.add_argument(
            "--no-members",
            action="store_false",
            dest="clean-members",
            default=True,
            help="Do not run full_clean for members",
        )
        parser.add_argument(
            "--no-students",
            action="store_false",
            dest="clean-students",
            default=True,
            help="Do not run full_clean for students",
        )
        parser.add_argument(
            "--no-alumni",
            action="store_false",
            dest="clean-alumni",
            default=True,
            help="Do not run full_clean for alumni",
        )
        parser.add_argument(
            "--save",
            action="store_true",
            dest="save",
            default=False,
            help="Perform save on models",
        )

    def clean_object(self, obj, options, person: Person, objectClass=Person):
        try:
            obj.full_clean()
            if options["save"]:
                obj.save()
        except objectClass.DoesNotExist:
            pass
        except ValidationError as e:
            stderr.write(
                f"Validation error in {obj.__class__.__name__} {BASE_URL}{person.id}/ - {e}\n"
            )

    def handle(self, *args, **options):
        persons = Person.objects.all().order_by("id")
        for person in persons:
            if options["clean-persons"]:
                self.clean_object(person, options, person)

            if options["clean-members"]:
                self.clean_object(person.member, options, person, Member)

            if options["clean-students"]:
                self.clean_object(person.student, options, person, Student)

            if options["clean-alumni"]:
                self.clean_object(person.alumnus, options, person, Alumnus)
