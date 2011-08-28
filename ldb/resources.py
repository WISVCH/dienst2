from djangorestframework.resources import ModelResource
from ldb.models import *

class AlumnusResource(ModelResource):
    model = Alumnus
    fields = ('person_id', 'study', 'study_first_year', 'study_last_year')
    # ordering = ('person_id',)

class MemberResource(ModelResource):
    model = Member
    fields = ('person_id', 'date_from','date_to')
    # ordering = ('person_id',)

class PersonResource(ModelResource):
    model = Person
    fields = (
                'id', 'titles','initials','firstname','preposition','surname','postfix_titles',
                ('member', MemberResource),
                ('alumnus', AlumnusResource),
             )
    # ordering = ('person_id',)

class AlumnusFullResource(ModelResource):
    model = Alumnus
    fields = ('study', 'study_first_year', 'study_last_year',
              'study_research_group', 'study_paper', 'study_professor',
              'work_company', 'work_position', 'work_sector')
    # exclude = ('person')

class MemberFullResource(ModelResource):
    model = Member
    fields = ('date_from', 'date_to', 'date_paid', 'amount_paid',
              'associate_member', 'donating_member', 'merit_date_from',
              'merit_invitations', 'merit_history', 'honorary_date_from')
    # exclude = ('person')

class PersonFullResource(ModelResource):
    model = Person
    fields = ('entity',
              'titles', 'initials', 'firstname', 'preposition', 'surname',
              'postfix_titles', 'phone_mobile', 'gender', 'birthdate',
              'deceased', 'living_with', 'mail_announcements',
              'mail_company', 'ldap_username',
              ('member', MemberFullResource),
              ('alumnus', AlumnusFullResource))
    # include = (('member', MemberFullResource),
    #            ('alumnus', AlumnusFullResource))