import os
import sys
import django

from xlrd.xldate import xldate_as_tuple
import xlrd
from xlrd import open_workbook

# This will insert the parent directory to the path so we can import the settings.
sys.path.insert(0, os.path.normpath(sys.path[0]+"/.."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dienst2.settings")
django.setup();
from dienst2.settings import *

from ldb.models import Person, Student, Member
import ldb.admin
import reversion
import datetime
from django.db import transaction

# should have two columns, student number as first and some kind of true/false yes/no combination as the second.
book = open_workbook('exportstudienummers.xls')

studenten = book.sheet_by_index(0)

for index in range(0, studenten.nrows):
    def cell(i):
        if studenten.cell(index, i).value != None and studenten.cell(index, i).value != '':
            return studenten.cell(index, i).value
        else:
            return None

    with transaction.atomic(), reversion.create_revision():
        #student unknown at CSa or no longer a student
        if(cell(1) == None or cell(1) == 'Nee'):
            student_number = str(int(cell(0)))
            student = Student.objects.filter(student_number = student_number).first()
            if(student != None):
                p = student.person

                m = Member.objects.filter(person = p).first()
                if(m != None):
                    m.date_to = datetime.date(2015, 06, 23)
                    message = 'User membership & subscriptions revoked on %s. User is either unknown or no longer a student according to CSa.' % str(datetime.datetime.now())
                    reversion.set_comment(message)
                    p.comment += '\n' + message
                    if(m.merit_date_from == None and m.honorary_date_from == None):
                        p.machazine = False
                        p.christmas_card = False
                        p.mail_announcement = False
                        p.mail_company = False
                    p.save();
                    m.save();
                    student.save();
                    print 'Student with student number '+student_number+ ' is no longer active, membership ended.'
                else:
                    print 'Student with student number' + student_number + ' is not a member.'
            else:
                print 'Failed to find student with studentnumber ' + student_number
        #student still active at TU Delft
        else:
            student_number = str(int(cell(0)))
            student = Student.objects.filter(student_number = student_number).first()
            if(student != None):
                p = student.person
                message = 'User student membership confirmed by CSa user check on %s.' % str(datetime.datetime.now())
                reversion.set_comment(message)
                p.comment += '\n' + message
                student.date_verified = datetime.date(2015, 06, 23)
                p.save();
                student.save();
                print'Student with student number '+student_number+ ' is still active'
            else:
                print 'Failed to find student with studentnumber ' + student_number
