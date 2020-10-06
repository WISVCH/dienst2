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
        exclude = ("merit_history", "associate_member", "donating_member")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class AlumnusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnus
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


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
        if not "revision_comment" in self.validated_data:
            raise ParseError("revision_comment not set")
        action = self.context["view"].action
        api_user = self.context["request"].user.username
        revision_comment = self.validated_data["revision_comment"]
        del self.validated_data["revision_comment"]
        with reversion.create_revision():
            reversion.set_comment(revision_comment)
            ret = super(EntitySerializer, self).save()
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


class OrganizationSerializer(EntitySerializer):
    id = ReadOnlyField()

    class Meta:
        model = Organization
        fields = "__all__"
