from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _


from ldb.formTemplates.committee import Committee
from ldb.formTemplates.person import Person


@python_2_unicode_compatible
class CommitteeMembership(models.Model):
    class Meta:
        verbose_name = _('committee membership')
        verbose_name_plural = _('committee memberships')
        ordering = ['board', 'committee__name']

    # Django admin doesn't support nested inlines,
    # so we'll just link to Person instead.
    person = models.ForeignKey(
        Person, related_name="committee_memberships", on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    board = models.IntegerField(_('board'))
    position = models.CharField(_('position'), max_length=50, blank=True)
    ras_months = models.IntegerField(_('RAS months'), blank=True, null=True)

    def __str__(self):
        return '[%s] %s - %s' % (self.board, self.committee, self.person)
