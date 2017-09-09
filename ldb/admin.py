from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from reversion_compare.admin import CompareVersionAdmin

from ldb.models import *


class CommitteeMembershipInline(admin.TabularInline):
    model = CommitteeMembership
    extra = 3


class StudentInline(admin.StackedInline):
    model = Student
    fieldsets = [
        (_('Base'), {'fields': ['study', 'first_year', 'student_number', 'enrolled']}),
        (_('Emergency'), {'fields': ['emergency_name', 'emergency_phone']}),
        (_('Permissions'), {'fields': ['yearbook_permission']}),
        (_('Other'), {'fields': ['date_verified']})
    ]


class MemberInline(admin.StackedInline):
    model = Member
    fieldsets = [
        (_('Base'), {'fields': ['date_from', 'date_to', 'date_paid', 'amount_paid']}),
        (_('Other'), {'fields': ['associate_member', 'donating_member']}),
        (_('Merit'), {'fields': ['merit_date_from', 'merit_invitations', 'merit_history']}),
        (_('Honorary'), {'fields': ['honorary_date_from']})
    ]


class AlumnusInline(admin.StackedInline):
    model = Alumnus
    fieldsets = [
        (_('Study'), {'fields': ['study', 'study_first_year', 'study_last_year',
                                 'study_research_group', 'study_paper', 'study_professor']}),
        (_('Work'), {'fields': ['work_company', 'work_position', 'work_sector']}),
    ]


class EmployeeInline(admin.StackedInline):
    model = Employee
    fieldsets = [
        (_('Base'), {'fields': ['faculty', 'department', 'function']}),
        (_('Phone'), {'fields': ['phone_internal']}),
    ]


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwds):
        super(PersonAdminForm, self).__init__(*args, **kwds)
        self.fields['living_with'].queryset = Person.objects.order_by('surname', 'firstname')


@admin.register(Person)
class PersonAdmin(CompareVersionAdmin):
    list_display = ('__str__', '_membership_status')

    form = PersonAdminForm
    fieldsets = [
        (_('Name'), {'fields': ['titles', 'initials', 'firstname', 'preposition',
                                'surname', 'postfix_titles']}),
        (_('Address'), {'fields': ['street_name', 'house_number', 'postcode',
                                   'address_2', 'address_3',
                                   'city', 'country', 'email', 'living_with']}),
        (_('Phone'), {'fields': ['phone_fixed', 'phone_mobile']}),
        (_('Accounts'), {'fields': ['ldap_username', 'netid', 'linkedin_id', 'facebook_id']}),
        (_('Other'), {'fields': ['gender', 'birthdate', 'deceased', 'comment']}),
        (_('Subscriptions'), {'fields': ['machazine', 'board_invites', 'constitution_card',
                                         'christmas_card', 'yearbook',
                                         'mail_announcements', 'mail_company', 'mail_education']}),
    ]
    inlines = [MemberInline, CommitteeMembershipInline, StudentInline, AlumnusInline, EmployeeInline]

    # Make sure we save inlines before saving Person - http://stackoverflow.com/a/29231611/2354734
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # call super method if object has no primary key
            super(PersonAdmin, self).save_model(request, obj, form, change)
        else:
            pass  # don't actually save the parent instance

    def save_formset(self, request, form, formset, change):
        formset.save()  # this will save the children
        form.instance.save()  # form.instance is the parent


@admin.register(Organization)
class OrganizationAdmin(CompareVersionAdmin):
    fieldsets = [
        (_('Base'), {'fields': ['name_prefix', 'name', 'name_short', 'salutation']}),
        (_('Address'), {'fields': ['street_name', 'house_number', 'postcode',
                                   'address_2', 'address_3',
                                   'city', 'country', 'email']}),
        (_('Phone'), {'fields': ['phone_fixed']}),
        (_('Subscriptions'), {'fields': ['machazine', 'constitution_card', 'yearbook',
                                         'christmas_card', 'board_invites']}),
        (_('Other'), {'fields': ['comment']})
    ]


admin.site.register(Committee, CompareVersionAdmin)

admin.site.register(Modification, admin.ModelAdmin)
