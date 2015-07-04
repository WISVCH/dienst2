import django_filters
from rest_framework import viewsets

from ldb.models import Person, Organization
from ldb.serializers import PersonSerializer, OrganizationSerializer


class PersonFilter(django_filters.FilterSet):
    netid = django_filters.CharFilter(name='netid', lookup_type='iexact')
    ldap_username = django_filters.CharFilter(name='ldap_username', lookup_type='iexact')

    class Meta:
        model = Person
        fields = ['ldap_username', 'netid', 'student__student_number']


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_class = PersonFilter


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
