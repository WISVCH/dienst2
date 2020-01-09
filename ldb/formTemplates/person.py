# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from dienst2.extras import CharNullField
from ldb.querysets import PersonQuerySet
from ldb.formTemplates.entity import Entity, get_attributes
from ldb.formTemplates.membershipStatus import MembershipStatus
from ldb.formTemplates.membershipStatusField import MembershipStatusField
from django.core.exceptions import ObjectDoesNotExist



@python_2_unicode_compatible
class Person(Entity):
    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    # Name
    titles = models.CharField(_('titles'), max_length=20, blank=True)
    initials = models.CharField(_('initials'), max_length=15)
    firstname = models.CharField(_('first name'), max_length=50)
    preposition = models.CharField(
        _('preposition'), max_length=15, blank=True)  # Tussenvoegsel
    surname = models.CharField(_('surname'), max_length=100)
    postfix_titles = models.CharField(
        _('postfix titles'), max_length=20, blank=True)

    # Telephone
    phone_mobile = models.CharField(
        _('phone mobile'), max_length=16, blank=True)

    # Other
    gender = models.CharField(
        _('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)

    deceased = models.BooleanField(_('deceased'), default=False)
    # https://code.djangoproject.com/ticket/7689
    # _living_with     =models.ManyToManyField('self')
    living_with = models.OneToOneField(
        'self', blank=True, null=True, on_delete=models.SET_NULL)

    # Subscriptions
    mail_announcements = models.BooleanField(
        _('announcements mailing'), default=True)
    mail_company = models.BooleanField(_('company mailing'), default=True)
    mail_education = models.BooleanField(_('education mailing'), default=True)

    ldap_username = CharNullField(
        _('LDAP username'), max_length=64, blank=True, null=True, unique=True)

    # External Accounts
    netid = CharNullField(_('NetID'), max_length=64,
                          blank=True, null=True, unique=True)
    linkedin_id = CharNullField(
        _('LinkedIn ID'), max_length=64, blank=True, null=True, unique=True)
    facebook_id = CharNullField(
        _('Facebook ID'), max_length=64, blank=True, null=True, unique=True)

    # Membership status
    _membership_status = MembershipStatusField(enum=MembershipStatus, db_column='membership_status',
                                               default=MembershipStatus.NONE)

    _original_living_with_id = None

    objects = PersonQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self._original_living_with_id = self.living_with_id

    @property
    def membership_status(self):
        try:
            member = self.member
        except ObjectDoesNotExist:
            return MembershipStatus.NONE
        if member.current_honorary_member:
            return MembershipStatus.HONORARY
        if member.current_merit_member:
            return MembershipStatus.MERIT
        if member.current_associate_member:
            return MembershipStatus.ASSOCIATE
        if member.current_regular_member:
            return MembershipStatus.REGULAR
        if member.current_alumnus_member:
            return MembershipStatus.ALUMNUS
        if member.current_donating_member:
            return MembershipStatus.DONATING
        else:
            return MembershipStatus.NONE

    @property
    def valid_membership_status(self):
        # We cannot do this in clean() because children aren't saved then,
        # and we can't do this in save() because we can't raise nice errors there.
        try:
            member = self.member
            if member.current_member and self.membership_status == MembershipStatus.NONE:
                return False
        except ObjectDoesNotExist:
            return True

    @property
    def formatted_name(self):
        strings = [self.titles, self.initials,
                   self.preposition, self.surname, self.postfix_titles]
        return ' '.join(filter(None, strings))

    @property
    def subscriptions(self):
        return get_attributes(self, ['machazine', 'constitution_card',
                                     'christmas_card', 'board_invites',
                                     'mail_announcements', 'mail_company', 'mail_education'])

    @property
    def gender_symbol(self):
        if self.gender == 'M':
            return '♂'
        elif self.gender == 'F':
            return '♀'
        else:
            return

    @property
    def age(self):
        born = self.birthdate
        today = date.today()
        try:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day - 1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def save(self, **kwargs):
        self._membership_status = self.membership_status

        super(Person, self).save(**kwargs)
        if self.pk is not None:
            old = self._original_living_with_id
            if old != self.living_with_id and old:
                other = Person.objects.get(pk=old)
                if other.living_with == self:
                    other.living_with = None
                    other.save()
            if self.living_with:
                other = self.living_with
                # Avoid save loops
                if other.living_with != self or \
                    other.street_name != self.street_name or \
                    other.house_number != self.house_number or \
                    other.address_2 != self.address_2 or \
                    other.address_3 != self.address_3 or \
                    other.postcode != self.postcode or \
                    other.city != self.city or \
                    other.country != self.country:
                    other.living_with = self
                    other.street_name = self.street_name
                    other.house_number = self.house_number
                    other.address_2 = self.address_2
                    other.address_3 = self.address_3
                    other.postcode = self.postcode
                    other.city = self.city
                    other.country = self.country
                    other.save()
        self.__original_living_with = self.living_with

    def if_student_number(self):
        if hasattr(self, 'student'):
            return self.student.student_number
        else:
            return None

    def get_absolute_url(self):
        return reverse('ldb_people_detail', args=[str(self.id)])

    def __str__(self):
        return ('%s, %s %s%s' %
                (self.surname, self.firstname, self.preposition, ' ✝' if self.deceased else '')).strip()
