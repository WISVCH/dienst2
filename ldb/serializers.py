import logging

import reversion
from drf_writable_nested.mixins import NestedCreateMixin, NestedUpdateMixin
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.fields import CharField, ReadOnlyField

from ldb.models import (
    Alumnus,
    CommitteeMembership,
    Employee,
    Entity,
    Member,
    Organization,
    Person,
    Student,
)

logger = logging.getLogger(__name__)


class MemberSerializer(serializers.ModelSerializer):
    current_member = ReadOnlyField()
    current_associate_member = ReadOnlyField()
    current_donating_member = ReadOnlyField()
    current_merit_member = ReadOnlyField()
    current_honorary_member = ReadOnlyField()

    class Meta:
        model = Member
        exclude = ("merit_history", "associate_member", "donating_member", "person")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ["person"]


class AlumnusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnus
        exclude = ["person"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["person"]


class CommitteeMembershipSerializer(serializers.ModelSerializer):
    committee = serializers.StringRelatedField()

    class Meta:
        model = CommitteeMembership
        exclude = ("ras_months",)


class EntitySerializer(
    NestedCreateMixin, NestedUpdateMixin, serializers.HyperlinkedModelSerializer
):
    street_address = ReadOnlyField()
    formatted_address = ReadOnlyField()
    country_full = ReadOnlyField(source="get_country_display")

    revision_comment = CharField(required=True, write_only=True)

    class Meta:
        model = Entity
        fields = "__all__"

    def save(self):
        if "revision_comment" not in self.validated_data:
            raise ParseError("revision_comment not set")
        action = self.context["view"].action
        api_user = self.context["request"].user.username
        revision_comment = self.validated_data["revision_comment"]
        del self.validated_data["revision_comment"]
        with reversion.create_revision():
            reversion.set_comment(revision_comment)
            ret = super().save()
        logger.info(
            "%s through API: %s %d (%s)", api_user, action, ret.pk, revision_comment
        )


class PersonSerializer(EntitySerializer):
    id = ReadOnlyField()
    member = MemberSerializer(partial=True)
    student = StudentSerializer(partial=True)
    alumnus = AlumnusSerializer(partial=True)
    employee = EmployeeSerializer(partial=True)
    living_with = serializers.HyperlinkedRelatedField(
        view_name="person-detail", read_only=True
    )
    committee_memberships = CommitteeMembershipSerializer(many=True, read_only=True)
    age = ReadOnlyField()
    membership_status = ReadOnlyField(source="_membership_status")
    formatted_name = ReadOnlyField()

    class Meta:
        model = Person
        exclude = ("comment", "_membership_status")

    def create(self, validated_data):
        # create employee entry
        employee_data = validated_data.pop("employee")
        alumnus_data = validated_data.pop("alumnus")
        member_data = validated_data.pop("member")
        student_data = validated_data.pop("student")

        person = Person.objects.create(**validated_data)

        Employee.objects.create(person=person, **employee_data)
        Alumnus.objects.create(person=person, **alumnus_data)
        Member.objects.create(person=person, **member_data)
        Student.objects.create(person=person, **student_data)

        return person


class OrganizationSerializer(EntitySerializer):
    id = ReadOnlyField()

    class Meta:
        model = Organization
        fields = "__all__"
