# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from dienst2.extras import CharNullField
from ldb.formTemplates.person import Person


@python_2_unicode_compatible
class Student(models.Model):
    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    person = models.OneToOneField(
        Person, primary_key=True, on_delete=models.CASCADE)

    enrolled = models.BooleanField(_('enrolled'), default=True)
    study = models.CharField(_('study'), max_length=50)
    first_year = models.IntegerField(_('first year'), blank=True, null=True)
    student_number = CharNullField(
        _('student number'), max_length=7, blank=True, null=True, unique=True)

    emergency_name = models.CharField(
        _('emergency name'), max_length=48, blank=True)
    emergency_phone = models.CharField(
        _('emergency phone'), max_length=16, blank=True)

    yearbook_permission = models.BooleanField(
        _('yearbook permission'), default=True)

    date_verified = models.DateField(_('date verified'), blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.student_number, str(self.person))
