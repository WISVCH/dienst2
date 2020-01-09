from __future__ import unicode_literals

import django_filters

from ldb.formTemplates.committeeMemberShip import CommitteeMembership


class CommitteeMembershipFilter(django_filters.FilterSet):

    class Meta:
        model = CommitteeMembership
        fields = ('board', 'committee')
