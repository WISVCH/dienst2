from ldb.models import *
from django.contrib import admin
from reversion.admin import VersionAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _

class CommitteeMembershipInline(admin.TabularInline):
    model = CommitteeMembership
    extra = 3

class StudentInline(admin.StackedInline):
    model = Student
    fieldsets = [
        (_('Base'),        {'fields': ['study', 'first_year', 'student_number', 'graduated']}),
        (_('Phone'),       {'fields': ['phone_parents']}),
        (_('Permissions'), {'fields': ['yearbook_permission']}),
        (_('Other'),       {'fields': ['date_verified']})
    ]
    
class MemberInline(admin.StackedInline):
    model = Member
    fieldsets = [
        (_('Base'),     {'fields': ['date_from', 'date_to', 'date_paid', 'amount_paid']}),
        (_('Other'),    {'fields': ['associate_member', 'donating_member']}),
        (_('Merit'),    {'fields': ['merit_date_from', 'merit_invitations', 'merit_history']}),
        (_('Honorary'), {'fields': ['honorary_date_from']})
    ]

class AlumnusInline(admin.StackedInline):
    model = Alumnus
    fieldsets = [
        (_('Study'), {'fields': ['study', 'study_first_year', 'study_last_year',
                                 'study_research_group', 'study_paper', 'study_professor']}),
        (_('Work'),  {'fields': ['work_company', 'work_position', 'work_sector']}),
    ]

class EmployeeInline(admin.StackedInline):
    model = Employee
    fieldsets = [
        (_('Base'),  {'fields': ['faculty', 'department', 'function']}),
        (_('Phone'), {'fields': ['phone_internal']}),
    ]

class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwds):
        super(PersonAdminForm, self).__init__(*args, **kwds)
        self.fields['living_with'].queryset = Person.objects.order_by('surname', 'firstname')

class PersonAdmin(VersionAdmin):
    form = PersonAdminForm
    fieldsets = [
        (_('Name'),          {'fields': ['titles', 'initials', 'firstname', 'preposition',
                                         'surname', 'postfix_titles']}),
        (_('Address'),       {'fields': ['street_name', 'house_number', 'postcode',
                                         'address_2', 'address_3',
                                         'city', 'country', 'email', 'living_with']}),
        (_('Phone'),         {'fields': ['phone_fixed', 'phone_mobile']}),
        (_('Accounts'),      {'fields': ['ldap_username', 'netid', 'linkedin_id', 'facebook_id']}),
        (_('Other'),         {'fields': ['gender', 'birthdate', 'deceased', 'comment']}),
        (_('Subscriptions'), {'fields': ['machazine', 'board_invites', 'constitution_card',
                                         'christmas_card', 'yearbook',
                                         'mail_announcements', 'mail_company']}),
    ]
    inlines = [MemberInline, CommitteeMembershipInline, StudentInline, AlumnusInline, EmployeeInline]
admin.site.register(Person, PersonAdmin)

class OrganizationAdmin(VersionAdmin):
    fieldsets = [
        (_('Base'),          {'fields': ['name_prefix', 'name', 'name_short', 'salutation']}),
        (_('Address'),       {'fields': ['street_name', 'house_number', 'postcode',
                                         'address_2', 'address_3',
                                         'city', 'country', 'email']}),
        (_('Phone'),         {'fields': ['phone_fixed']}),
        (_('Subscriptions'), {'fields': ['machazine', 'constitution_card', 'yearbook',
                                         'christmas_card', 'board_invites']}),
        (_('Other'),         {'fields': ['comment']})
    ]
admin.site.register(Organization, OrganizationAdmin)

admin.site.register(Committee, VersionAdmin)

class ItemAdmin(VersionAdmin):
  """ItemAdmin"""

admin.site.register(Modification, VersionAdmin)
