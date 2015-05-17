from rest_framework import serializers
from rest_framework.fields import IntegerField, ReadOnlyField

from ldb.models import Person, Member, Student, Employee, Alumnus, CommitteeMembership, Organization


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ('merit_history',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student


class AlumnusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnus


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

class CommitteeMembershipSerializer(serializers.ModelSerializer):
    committee = serializers.StringRelatedField()

    class Meta:
        model = CommitteeMembership

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    id = ReadOnlyField()
    member = MemberSerializer()
    student = StudentSerializer()
    alumnus = AlumnusSerializer()
    employee = EmployeeSerializer()
    living_with = serializers.HyperlinkedRelatedField(view_name='person-detail', read_only=True)
    committees = CommitteeMembershipSerializer(many=True, read_only=True)
    age = ReadOnlyField()

    class Meta:
        model = Person
        exclude = ('comment',)

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    id = ReadOnlyField()

    class Meta:
        model = Organization
