from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from ldb.models import *
from django.utils.translation import ugettext as _

class PersonForm(ModelForm):
    class Meta:
        model = Person

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

MemberFormSet = inlineformset_factory(Person, Member, form=ModelForm)
StudentFormSet = inlineformset_factory(Person, Student, form=ModelForm)
AlumnusFormSet = inlineformset_factory(Person, Alumnus, form=ModelForm)
EmployeeFormSet = inlineformset_factory(Person, Employee, form=ModelForm)
CommitteeMembershipFormSet = inlineformset_factory(Person, CommitteeMembership, form=ModelForm, extra=3)