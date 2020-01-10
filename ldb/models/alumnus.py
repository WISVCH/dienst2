# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _
from ldb.models.person import Person

CONTACT_METHOD_CHOICES = (
    ('m', 'Mail'),
    ('e', 'Email'),
)


@python_2_unicode_compatible
class Alumnus(models.Model):
    class Meta:
        verbose_name = _('alumnus')
        verbose_name_plural = _('alumni')

    person = models.OneToOneField(
        Person, primary_key=True, on_delete=models.CASCADE)

    study = models.CharField(_('study'), max_length=100, blank=True)
    study_first_year = models.IntegerField(
        _('study first year'), blank=True, null=True)
    study_last_year = models.IntegerField(
        _('study last year'), blank=True, null=True)
    study_research_group = models.CharField(
        _('research group'), max_length=100, blank=True)
    study_paper = models.CharField(_('paper'), max_length=300, blank=True)
    study_professor = models.CharField(
        _('professor'), max_length=100, blank=True)

    work_company = models.CharField(_('company'), max_length=100, blank=True)
    work_position = models.CharField(_('position'), max_length=100, blank=True)
    work_sector = models.CharField(_('sector'), max_length=100, blank=True)

    contact_method = models.CharField(
        _('contact method'), max_length=1, choices=CONTACT_METHOD_CHOICES, default='e')

    def __str__(self):
        return str(self.person)
