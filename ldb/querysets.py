from django.db.models import QuerySet


class EntityQuerySet(QuerySet):
    pass


class PersonQuerySet(EntityQuerySet):
    """
    The QuerySet to be used for persons.

    Here we can declare default filters that are often used.
    """

    def members(self):
        from ldb.models.membershipStatus import MembershipStatus
        return self.filter(_membership_status__gte=MembershipStatus.REGULAR)
