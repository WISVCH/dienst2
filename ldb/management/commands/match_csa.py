import csv
import datetime

import reversion
from django.db import transaction
from django.core.management import BaseCommand

from ldb.models import Student, MembershipStatus


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=unicode)

        parser.add_argument('--yes-value',
                            dest='yes-value',
                            default='ja',
                            help='Define which value is in the document when the CSa says the person is still a student')
        parser.add_argument('--date',
                            dest='date',
                            default=None,
                            help='Date on which CSa provided the document')

    def handle(self, *args, **options):
        if options['date']:
            date = datetime.datetime.strptime(options['date'], '%Y-%m-%d').date()
        else:
            date = datetime.date.today()

        with open(options['file']) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                with transaction.atomic(), reversion.create_revision():
                    student_number = row[0]

                    try:
                        student = Student.objects.get(student_number=student_number)
                    except Student.DoesNotExist:
                        self.stderr.write("Failed to find student with student number '{}' in database".format(student_number))
                        continue

                    person = student.person

                    if not row[1].lower() == options['yes-value'].lower():
                        student.enrolled = False
                        student.save()

                        if person.membership_status == MembershipStatus.REGULAR:
                            member = person.member
                            member.date_to = date

                            message = 'Membership revoked. Student is either unknown or no longer a student according to CSa.'
                            reversion.set_comment(message)

                            member.save()

                            self.stdout.write("Student with student number '{}' is no longer active, membership ended.".format(student_number))
                    else:
                        reversion.set_comment('Student confirmed by CSa')
                        student.date_verified = date
                        self.stdout.write("Student with student number '{}' is still active".format(student_number))
                        student.save()

                    # Person is saved so the reversion revision is made
                    person.save()
