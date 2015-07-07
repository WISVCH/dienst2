from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from ldb.models import Person


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--no-persons',
                            action='store_false',
                            dest='clean-persons',
                            default=True,
                            help='Do not run full_clean for persons')
        parser.add_argument('--no-members',
                            action='store_false',
                            dest='clean-members',
                            default=True,
                            help='Do not run full_clean for members')
        parser.add_argument('--no-students',
                            action='store_false',
                            dest='clean-students',
                            default=True,
                            help='Do not run full_clean for students')
        parser.add_argument('--save',
                            action='store_true',
                            dest='save',
                            default=False,
                            help='Perform save on models')

    def handle(self, *args, **options):
        persons = Person.objects.all()
        for person in persons:
            if options['clean-persons']:
                try:
                    person.full_clean()
                except ValidationError:
                    self.stderr(
                        'Validation error in Person https://frans.chnet/dienst2/admin/ldb/person/{}/'.format(person.id))

                if options['save']:
                        person.save()

            if options['clean-members']:
                try:
                    person.member.full_clean()
                except ValidationError:
                    self.stderr(
                        'Validation error in Member https://frans.chnet/dienst2/admin/ldb/person/{}/'.format(person.id))

                if options['save']:
                        person.member.save()

            if options['clean-students']:
                try:
                    person.student.full_clean()
                except ValidationError:
                    self.stderr(
                        'Validation error in Student https://frans.chnet/dienst2/admin/ldb/person/{}/'.format(person.id))

                if options['save']:
                        person.student.save()
