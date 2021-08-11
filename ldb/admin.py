from __future__ import unicode_literals

import datetime
import math

from django import forms
from django.contrib import admin
from django.db.models import Q
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from import_export import resources, widgets
from reversion_compare.admin import CompareVersionAdmin

from ldb.ImportExportVersionModelAdmin import ImportExportVersionModelAdmin
from ldb.models import *


class CommitteeMembershipInline(admin.TabularInline):
    model = CommitteeMembership
    extra = 3


class StudentInline(admin.StackedInline):
    model = Student
    fieldsets = [
        (_("Base"), {"fields": ["study", "first_year", "student_number", "enrolled"]}),
        (_("Emergency"), {"fields": ["emergency_name", "emergency_phone"]}),
        (_("Permissions"), {"fields": ["yearbook_permission"]}),
        (_("Other"), {"fields": ["date_verified"]}),
    ]


class MemberInline(admin.StackedInline):
    model = Member
    fieldsets = [
        (_("Base"), {"fields": ["date_from", "date_to", "date_paid", "amount_paid"]}),
        (_("Other"), {"fields": ["associate_member", "donating_member"]}),
        (
            _("Merit"),
            {"fields": ["merit_date_from", "merit_invitations", "merit_history"]},
        ),
        (_("Honorary"), {"fields": ["honorary_date_from"]}),
    ]


class AlumnusInline(admin.StackedInline):
    model = Alumnus
    fieldsets = [
        (
            _("Study"),
            {
                "fields": [
                    "study",
                    "study_first_year",
                    "study_last_year",
                    "study_research_group",
                    "study_paper",
                    "study_professor",
                ]
            },
        ),
        (_("Work"), {"fields": ["work_company", "work_position", "work_sector"]}),
    ]


class EmployeeInline(admin.StackedInline):
    model = Employee
    fieldsets = [
        (_("Base"), {"fields": ["faculty", "department", "function"]}),
        (_("Phone"), {"fields": ["phone_internal"]}),
    ]


class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    def __init__(self, *args, **kwds):
        super(PersonAdminForm, self).__init__(*args, **kwds)
        self.fields["living_with"].queryset = Person.objects.order_by(
            "surname", "firstname"
        )


class PersonResource(resources.ModelResource):
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        if "id" not in dataset.headers:
            dataset.lpush_col([None for row in range(len(dataset))], header="id")

    def init_instance(self, row=None):
        instance = self._meta.model()
        try:
            student = Student.objects.get(
                student_number=str(
                    row["student__student_number"]
                )  # Cast to string as it is saved like this in the DB
            )
        except Student.DoesNotExist:
            student = Student()

        try:
            member = Member.objects.get(person_id=row["id"])
        except Member.DoesNotExist:
            member = Member()

        instance.member = member
        instance.student = student
        return instance

    def get_or_init_instance(self, instance_loader, row):
        """
        Either fetches an already existing instance or initializes a new one.
        """
        try:
            instance = Person.objects.get(
                Q(netid=str(row["netid"]))
                | Q(student__student_number=str(row["student__student_number"]))
            )
        except Person.DoesNotExist:
            instance = None

        if instance:
            return instance, False
        else:
            return self.init_instance(row), True

    def import_obj(self, obj, data, dry_run):
        """
        Traverses every field in this Resource and calls
        :meth:`~import_export.resources.Resource.import_field`. If
        ``import_field()`` results in a ``ValueError`` being raised for
        one of more fields, those errors are captured and reraised as a single,
        multi-field ValidationError."""
        errors = {}

        for field in self.get_import_fields():
            if str.startswith(field.attribute, "student__") or str.startswith(
                field.attribute, "member__"
            ):
                continue
            if isinstance(field.widget, widgets.ManyToManyWidget):
                continue
            try:
                self.import_field(field, obj, data)
            except ValueError as e:
                errors[field.attribute] = ValidationError(force_text(e), code="invalid")

        # Student validation
        obj.student.yearbook_permission = bool(data["student__yearbook_permission"])
        obj.student.first_year = data["student__first_year"]
        obj.student.study = str(data["student__study"])
        obj.student.student_number = str(data["student__student_number"])
        obj.student.emergency_phone = str(data["student__emergency_phone"])
        obj.student.emergency_name = str(data["student__emergency_name"])

        try:
            obj.student.full_clean(exclude="person")
        except ValidationError as e:
            for key, value in e:
                if key != "person":
                    errors["student__" + key] = ValidationError(
                        force_text(value), code="invalid"
                    )

        # Member validation
        obj.member.amount_paid = data["member__amount_paid"]
        obj.member.date_from = datetime.datetime.today()
        obj.member.date_to = datetime.datetime.today().replace(
            year=datetime.datetime.today().year
            + math.ceil(data["member__amount_paid"] / 5)
        )

        try:
            obj.member.full_clean(exclude="person")
        except ValidationError as e:
            for key, value in e:
                if key != "person":
                    errors["member__" + key] = ValidationError(
                        force_text(value), code="invalid"
                    )

        if errors:
            raise ValidationError(errors)

    def after_save_instance(self, instance, using_transactions, dry_run):
        # Saving student
        instance.student.person_id = instance.id
        instance.student.save()
        # Saving member
        instance.member.person_id = instance.id
        instance.member.save()

    class Meta:
        model = Person
        use_transactions = True
        fields = export_order = (
            "id",
            "initials",
            "firstname",
            "preposition",
            "surname",
            "netid",
            "student__student_number",
            "street_name",
            "house_number",
            "postcode",
            "city",
            "country",
            "email",
            "phone_mobile",
            "gender",
            "birthdate",
            "student__yearbook_permission",
            "mail_announcements",
            "mail_company",
            "mail_education",
            "machazine",
            "student__first_year",
            "student__study",
            "student__emergency_phone",
            "student__emergency_name",
            "member__amount_paid",
        )
        skip_unchanged = True


@admin.register(Person)
class PersonAdmin(ImportExportVersionModelAdmin):
    list_display = ("__str__", "_membership_status")

    resource_class = PersonResource

    form = PersonAdminForm
    fieldsets = [
        (
            _("Name"),
            {
                "fields": [
                    "titles",
                    "initials",
                    "firstname",
                    "preposition",
                    "surname",
                    "postfix_titles",
                ]
            },
        ),
        (
            _("Address"),
            {
                "fields": [
                    "street_name",
                    "house_number",
                    "postcode",
                    "address_2",
                    "address_3",
                    "city",
                    "country",
                    "email",
                    "living_with",
                ]
            },
        ),
        (_("Phone"), {"fields": ["phone_fixed", "phone_mobile"]}),
        (
            _("Accounts"),
            {
                "fields": [
                    "ldap_username",
                    "email_forward",
                    "netid",
                    "linkedin_id",
                    "facebook_id",
                ]
            },
        ),
        (_("Other"), {"fields": ["gender", "birthdate", "deceased", "comment"]}),
        (
            _("Subscriptions"),
            {
                "fields": [
                    "machazine",
                    "board_invites",
                    "constitution_card",
                    "christmas_card",
                    "yearbook",
                    "mail_announcements",
                    "mail_company",
                    "mail_education",
                ]
            },
        ),
    ]
    inlines = [
        MemberInline,
        CommitteeMembershipInline,
        StudentInline,
        AlumnusInline,
        EmployeeInline,
    ]

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
        (_("Base"), {"fields": ["name_prefix", "name", "name_short", "salutation"]}),
        (
            _("Address"),
            {
                "fields": [
                    "street_name",
                    "house_number",
                    "postcode",
                    "address_2",
                    "address_3",
                    "city",
                    "country",
                    "email",
                ]
            },
        ),
        (_("Phone"), {"fields": ["phone_fixed"]}),
        (
            _("Subscriptions"),
            {
                "fields": [
                    "machazine",
                    "constitution_card",
                    "yearbook",
                    "christmas_card",
                    "board_invites",
                ]
            },
        ),
        (_("Other"), {"fields": ["comment"]}),
    ]


admin.site.register(Committee, CompareVersionAdmin)

admin.site.register(Modification, admin.ModelAdmin)
