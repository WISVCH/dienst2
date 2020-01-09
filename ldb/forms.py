from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from ldb.formTemplates.alumnus import Alumnus
from ldb.formTemplates.committeeMemberShip import CommitteeMembership
from ldb.formTemplates.employee import Employee
from ldb.formTemplates.member import Member
from ldb.formTemplates.organization import Organization
from ldb.formTemplates.person import Person
from ldb.formTemplates.student import Student


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('_membership_status',)


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


MemberFormSet = inlineformset_factory(Person, Member, form=ModelForm, fields="__all__")
StudentFormSet = inlineformset_factory(Person, Student, form=ModelForm, fields="__all__")
AlumnusFormSet = inlineformset_factory(Person, Alumnus, form=ModelForm, fields="__all__")
EmployeeFormSet = inlineformset_factory(Person, Employee, form=ModelForm, fields="__all__")
CommitteeMembershipFormSet = inlineformset_factory(Person, CommitteeMembership, form=ModelForm, extra=3,
                                                   fields="__all__")
