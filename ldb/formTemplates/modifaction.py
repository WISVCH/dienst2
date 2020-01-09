from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _


from ldb.formTemplates.person import Person


@python_2_unicode_compatible
class Modification(models.Model):
    class Meta:
        verbose_name = _('modification')
        verbose_name_plural = _('modifications')

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    ip = models.CharField(_('ip address'), max_length=40)
    modification = models.TextField(_('modification'), blank=True)

    def __str__(self):
        return 'Edit [%s] %s' % (self.date, self.person.__str__())
