from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _


from ldb.models.person import Person


@python_2_unicode_compatible
class Committee(models.Model):
    class Meta:
        verbose_name = _('committee')
        verbose_name_plural = _('committees')
        ordering = ['name']

    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    members = models.ManyToManyField(Person, through='CommitteeMembership')

    def __str__(self):
        return self.name
