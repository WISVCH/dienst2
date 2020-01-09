# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.six import python_2_unicode_compatible

from ldb.country_field import CountryField
from ldb.querysets import EntityQuerySet
from django.utils.translation import gettext as _


def get_attributes(self, attrs):
    v = {}
    for attr in attrs:
        v[self._meta.get_field(
            attr).verbose_name] = self.__getattribute__(attr)
    return v


@python_2_unicode_compatible
class Entity(models.Model):
    class Meta:
        verbose_name = _('entity')
        verbose_name_plural = _('entities')

    # Address
    street_name = models.CharField(_('street name'), max_length=75, blank=True)
    house_number = models.CharField(
        _('house number'), max_length=7, blank=True)
    address_2 = models.CharField(_('address row 2'), max_length=75, blank=True)
    address_3 = models.CharField(_('address row 3'), max_length=75, blank=True)
    postcode = models.CharField(_('postcode'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=50, blank=True)
    country = CountryField(_('country'), blank=True)
    email = models.EmailField(_('e-mail'), blank=True)

    # Telephone
    phone_fixed = models.CharField(_('phone fixed'), max_length=16, blank=True)

    # Subscriptions
    machazine = models.BooleanField(_('MaCHazine'), default=True)
    board_invites = models.BooleanField(_('board invites'), default=False)
    constitution_card = models.BooleanField(
        _('constitution card'), default=False)
    christmas_card = models.BooleanField(_('Christmas card'), default=True)
    yearbook = models.BooleanField(_('yearbook'), default=False)

    # Other
    comment = models.TextField(blank=True)

    objects = EntityQuerySet.as_manager()

    @property
    def street_address(self):
        strings = [self.street_name + ' ' +
                   self.house_number, self.address_2, self.address_3]
        return '\n'.join(filter(None, strings))

    @property
    def formatted_address(self):
        strings = [self.street_address, self.postcode + ('  ' + self.city.upper() if self.postcode != 'INTERN' else ''),
                   self.get_country_display() if self.country != 'NL' else '']
        return '\n'.join(filter(None, strings))

    @property
    def subscriptions(self):
        return get_attributes(self, ['machazine', 'board_invites', 'constitution_card',
                                     'christmas_card', 'yearbook'])

    def clean(self):
        if (self.street_name != '' or
            self.house_number != '' or
            self.address_2 != '' or
            self.address_3 != '' or
            self.postcode != '' or
            self.city != '') and self.country == '':
            raise ValidationError('Country is required if address is entered.')

    def __str__(self):
        return '%s %s, %s %s, %s' % (self.street_name, self.house_number,
                                     self.postcode, self.city, self.country)

    def set_address_incorrect(self):
        self.street_name = ''
        self.house_number = ''
        self.address_2 = ''
        self.address_3 = ''
        self.postcode = ''
        self.city = ''
        self.country = ''
