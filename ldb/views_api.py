from rest_framework import viewsets

from ldb.models import Person, Organization
from ldb.serializers import PersonSerializer, OrganizationSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_fields = ('ldap_username', 'netid', 'student__student_number')


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
