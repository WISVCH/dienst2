from __future__ import unicode_literals

from django.db.models import Prefetch
import django_filters
from rest_framework import viewsets

from ldb.models import Person, Organization, CommitteeMembership
from ldb.serializers import PersonSerializer, OrganizationSerializer


class PersonFilter(django_filters.FilterSet):
    netid = django_filters.CharFilter(name='netid', lookup_expr='iexact')
    ldap_username = django_filters.CharFilter(name='ldap_username', lookup_expr='iexact')

    class Meta:
        model = Person
        fields = ['ldap_username', 'netid', 'student__student_number']


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().select_related('member', 'student', 'alumnus', 'employee').prefetch_related(
        Prefetch('committee_memberships', queryset=CommitteeMembership.objects.select_related('committee')))
    filter_class = PersonFilter


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
