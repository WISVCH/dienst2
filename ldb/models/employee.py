from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _


from ldb.models.person import Person


@python_2_unicode_compatible
class Employee(models.Model):
    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    person = models.OneToOneField(
        Person, primary_key=True, on_delete=models.CASCADE)

    faculty = models.CharField(_('faculty'), max_length=50)
    department = models.CharField(_('department'), max_length=50)
    function = models.CharField(_('function'), max_length=50)
    phone_internal = models.CharField(_('phone internal'), max_length=5)

    def __str__(self):
        return str(self.person)
