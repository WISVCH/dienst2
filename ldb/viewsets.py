from __future__ import unicode_literals

import django_filters
from django.db.models import Prefetch
from rest_framework import viewsets

from ldb.models import Person, Organization, CommitteeMembership
from ldb.serializers import PersonSerializer, OrganizationSerializer


class PersonFilter(django_filters.FilterSet):
    netid = django_filters.CharFilter(field_name='netid', lookup_expr='iexact')
    ldap_username = django_filters.CharFilter(field_name='ldap_username', lookup_expr='iexact')

    class Meta:
        model = Person
        fields = ['ldap_username', 'netid', 'student__student_number']


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().select_related('member', 'student', 'alumnus', 'employee').prefetch_related(
        Prefetch('committee_memberships', queryset=CommitteeMembership.objects.select_related('committee')))
    filterset_class = PersonFilter


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
