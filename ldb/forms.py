from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from ldb.models import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ("_membership_status",)


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


MemberFormSet = inlineformset_factory(Person, Member, form=ModelForm, fields="__all__")
StudentFormSet = inlineformset_factory(
    Person, Student, form=ModelForm, fields="__all__"
)
AlumnusFormSet = inlineformset_factory(
    Person, Alumnus, form=ModelForm, fields="__all__"
)
EmployeeFormSet = inlineformset_factory(
    Person, Employee, form=ModelForm, fields="__all__"
)
CommitteeMembershipFormSet = inlineformset_factory(
    Person, CommitteeMembership, form=ModelForm, extra=3, fields="__all__"
)
