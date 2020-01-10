# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from ldb.models.entity import Entity
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _



@python_2_unicode_compatible
class Organization(Entity):
    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        manager_inheritance_from_future = True

    name_prefix = models.CharField(
        _('name prefix'), max_length=100, blank=True)
    name = models.CharField(_('name'), max_length=100)
    name_short = models.CharField(_('name short'), max_length=100, blank=True)
    salutation = models.CharField(_('salutation'), max_length=100)

    def get_absolute_url(self):
        return reverse('ldb_organizations_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.name)
