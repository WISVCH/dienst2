from sys import stderr

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from ldb.models import Person, Member, Student, Alumnus

BASE_URL = 'https://frans.chnet/dienst2'


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
        parser.add_argument('--no-alumni',
                            action='store_false',
                            dest='clean-alumni',
                            default=True,
                            help='Do not run full_clean for alumni')
        parser.add_argument('--save',
                            action='store_true',
                            dest='save',
                            default=False,
                            help='Perform save on models')

    def handle(self, *args, **options):
        persons = Person.objects.all().order_by('id')
        for person in persons:
            if options['clean-persons']:
                try:
                    person.full_clean()
                    if options['save']:
                        person.save()
                except ValidationError, e:
                    stderr.write('Validation error in Person {}/admin/ldb/person/{}/ - {}\n'
                                 .format(BASE_URL, person.id, e))

            if options['clean-members']:
                try:
                    person.member.full_clean()
                    if options['save']:
                        person.member.save()
                except Member.DoesNotExist:
                    pass
                except ValidationError, e:
                    stderr.write('Validation error in Member {}/admin/ldb/person/{} - {}/\n'
                                 .format(BASE_URL, person.id, e))

            if options['clean-students']:
                try:
                    person.student.full_clean()
                    if options['save']:
                        person.student.save()
                except Student.DoesNotExist:
                    pass
                except ValidationError, e:
                    stderr.write('Validation error in Student {}/admin/ldb/person/{}/ - {}\n'
                                 .format(BASE_URL, person.id, e))

            if options['clean-alumni']:
                try:
                    person.alumnus.full_clean()
                    if options['save']:
                        person.alumnus.save()
                except Alumnus.DoesNotExist:
                    pass
                except ValidationError, e:
                    stderr.write('Validation error in Alumnus {}/admin/ldb/person/{}/ - {}\n'
                                 .format(BASE_URL, person.id, e))
