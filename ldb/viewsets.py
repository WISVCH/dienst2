import django_filters
from django.db.models import Prefetch
from rest_framework import viewsets

from ldb.models import CommitteeMembership, Organization, Person
from ldb.serializers import OrganizationSerializer, PersonSerializer


class PersonFilter(django_filters.FilterSet):
    netid = django_filters.CharFilter(field_name='netid', lookup_expr='iexact')
    ldap_username = django_filters.CharFilter(field_name='ldap_username', lookup_expr='iexact')
    student__student_number = django_filters.CharFilter(field_name='student__student_number', label='Student number')

    class Meta:
        model = Person
        fields = ['ldap_username', 'netid', 'student__student_number']


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all() \
        .select_related('member', 'student', 'alumnus', 'employee') \
        .prefetch_related(Prefetch('committee_memberships',
                                   queryset=CommitteeMembership.objects.select_related('committee')))
    filterset_class = PersonFilter


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
