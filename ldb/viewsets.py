import django_filters
from django.db.models import Prefetch
from ldb.google import get_groups_by_user_key
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from googleapiclient.errors import HttpError
from ldb.models import CommitteeMembership, Organization, Person
from ldb.serializers import OrganizationSerializer, PersonSerializer


class PersonFilter(django_filters.FilterSet):
    netid = django_filters.CharFilter(field_name="netid", lookup_expr="iexact")
    ldap_username = django_filters.CharFilter(
        field_name="ldap_username", lookup_expr="iexact"
    )
    google_username = django_filters.CharFilter(
        field_name="google_username", lookup_expr="iexact"
    )
    student__student_number = django_filters.CharFilter(
        field_name="student__student_number", label="Student number"
    )

    class Meta:
        model = Person
        fields = [
            "ldap_username",
            "google_username",
            "netid",
            "student__student_number",
        ]


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = (
        Person.objects.all()
        .select_related("member", "student", "alumnus", "employee")
        .prefetch_related(
            Prefetch(
                "committee_memberships",
                queryset=CommitteeMembership.objects.select_related("committee"),
            )
        )
    )
    filterset_class = PersonFilter

    @action(detail=True, methods=["get"])
    def google_groups(self, request, pk=None):
        person = self.get_object()

        google_groups = []

        # Check if the person has a valid membership status
        if person.valid_membership_status is False:
            return Response(google_groups)

        # Check if the person has a google username
        if person.google_username is None:
            return Response(google_groups)

        # Retrieve the groups from the Directory API
        try:
            google_groups = get_groups_by_user_key(
                person.google_username + "@ch.tudelft.nl"
            )
        except HttpError as e:
            if e.resp.status == 404:
                return Response(google_groups)
            else:
                raise e

            return Response([])

        return Response(google_groups)


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
