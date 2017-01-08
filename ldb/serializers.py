from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from ldb.models import Person, Member, Student, Employee, Alumnus, CommitteeMembership, Organization, Entity


class MemberSerializer(serializers.ModelSerializer):
    current_member = ReadOnlyField()
    current_associate_member = ReadOnlyField()
    current_donating_member = ReadOnlyField()
    current_merit_member = ReadOnlyField()
    current_honorary_member = ReadOnlyField()

    class Meta:
        model = Member
        exclude = ('merit_history', 'associate_member', 'donating_member',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AlumnusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnus
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class CommitteeMembershipSerializer(serializers.ModelSerializer):
    committee = serializers.StringRelatedField()

    class Meta:
        model = CommitteeMembership
        exclude = ('ras_months',)


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    street_address = ReadOnlyField()
    formatted_address = ReadOnlyField()
    country_full = ReadOnlyField(source='get_country_display')

    class Meta:
        model = Entity
        fields = '__all__'


class PersonSerializer(EntitySerializer):
    id = ReadOnlyField()
    member = MemberSerializer()
    student = StudentSerializer()
    alumnus = AlumnusSerializer()
    employee = EmployeeSerializer()
    living_with = serializers.HyperlinkedRelatedField(view_name='person-detail', read_only=True)
    committee_memberships = CommitteeMembershipSerializer(many=True, read_only=True)
    age = ReadOnlyField()
    membership_status = ReadOnlyField(source='_membership_status')
    formatted_name = ReadOnlyField()

    class Meta:
        model = Person
        exclude = ('comment', '_membership_status')


class OrganizationSerializer(EntitySerializer):
    id = ReadOnlyField()

    class Meta:
        model = Organization
        fields = '__all__'
