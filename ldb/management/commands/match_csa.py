import datetime

import reversion
from django.db import transaction
from xlrd import open_workbook
from django.core.management import BaseCommand

from ldb.models import Student, Member


def cell(sheet, row, col):
    value = sheet.cell(row, col).value
    if value and value != '':
        return value
    else:
        return None


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1, type=unicode)

        parser.add_argument('--yes-value',
                            dest='yes-value',
                            default='ja',
                            help='Define which value is in the document when the CSa says the person is still a student')

    def check_is_student(self, studenten, row, yes_value):
        value = cell(studenten, row, 1)
        return value.lower() == yes_value.lower()

    def get_student_number(self, studenten, row):
        return str(int(cell(studenten, row, 0)))

    def handle(self, *args, **options):
        book = open_workbook(options['file'])
        studenten = book.sheet_by_index(0)

        for row in range(0, studenten.nrows):
            with transaction.atomic(), reversion.create_revision():
                student_number = self.get_student_number(studenten, row)

                try:
                    student = Student.objects.get(student_number=student_number)
                except Student.DoesNotExist:
                    self.stderr("Failed to find student with student number '{}' in database".format(student_number))
                    continue

                person = student.person

                if not self.check_is_student(studenten, row, options['yes-value']):
                    try:
                        member = person.member
                    except Member.DoesNotExist:
                        self.stderr("Student with student number '{}' does not have a connected member model".format(student_number))
                        continue

                    # Do not change member-models if: membership already revoked, is merit member or is honorary member
                    if member.date_to is not None or member.merit_date_from is not None or member.honorary_date_from is not None:
                        continue

                    member.date_to = datetime.date.today()

                    message = 'Membership revoked. Student is either unknown or no longer a student according to CSa.'
                    reversion.set_comment(message)

                    member.save()

                    self.stdout("Student with student number '{}' is no longer active, membership ended.".format(student_number))
                else:
                    reversion.set_comment('Student confirmed by CSa')
                    student.date_verified = datetime.date.today()
                    self.stdout("Student with student number '{}' is still active".format(student_number))

                student.save()
                # Person is saved so the reversion revision is made
                person.save()
