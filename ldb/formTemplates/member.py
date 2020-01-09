# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ldb.formTemplates.alumnus import Alumnus
from ldb.formTemplates.person import Person
from ldb.formTemplates.student import Student


@python_2_unicode_compatible
class Member(models.Model):
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    person = models.OneToOneField(
        Person, primary_key=True, on_delete=models.CASCADE)

    date_from = models.DateField(_('date from'), blank=True, null=True)
    date_to = models.DateField(_('date to'), blank=True, null=True)
    date_paid = models.DateField(_('date paid'), blank=True, null=True)
    amount_paid = models.IntegerField(_('amount paid'), blank=True, null=True)

    associate_member = models.BooleanField(
        _('associate member'), default=False)
    donating_member = models.BooleanField(_('donating member'), default=False)

    merit_date_from = models.DateField(
        _('merit member date from'), blank=True, null=True)
    merit_invitations = models.BooleanField(
        _('merit member invitations'), default=True)
    merit_history = models.TextField(_('merit member history'), blank=True)

    honorary_date_from = models.DateField(
        _('honorary member from date'), blank=True, null=True)

    @property
    def current_member(self):
        return self.date_from is not None and (self.date_to is None or self.date_to > date.today()) \
            and not self.person.deceased

    @property
    def current_regular_member(self):
        try:
            student = self.person.student
            return student.enrolled and self.current_member
        except Student.DoesNotExist:
            return False

    @property
    def current_alumnus_member(self):
        return self.current_member and \
            Alumnus.objects.filter(person=self.person).exists() > 0 and \
            not self.current_regular_member

    @property
    def current_associate_member(self):
        return self.associate_member and self.current_member

    @property
    def current_donating_member(self):
        return self.donating_member and self.current_member

    @property
    def current_merit_member(self):
        return self.merit_date_from is not None and self.current_member

    @property
    def current_honorary_member(self):
        return self.honorary_date_from is not None and self.current_member

    def __str__(self):
        return str(self.person)

    def clean(self):
        if (self.date_from is not None and self.date_to is not None and self.date_from > self.date_to) or \
           (self.date_to is not None and self.date_from is None):
            raise ValidationError("'Date to' cannot be before 'date from'")

        if self.date_to is not None and (self.merit_date_from is not None or self.honorary_date_from is not None):
            raise ValidationError(
                "'Date to' cannot be set for merit and honorary members")

        if self.merit_date_from is not None and self.merit_date_from > date.today():
            raise ValidationError("Merit date from should be in the past")

        if self.honorary_date_from is not None and self.honorary_date_from > date.today():
            raise ValidationError("Honorary date from should be in the past")

        if self.merit_date_from is not None and self.date_from is None:
            raise ValidationError("Cannot have a 'merit from date' without a 'date from'. (Merit member must be a "
                                  "regular member too)")

        if self.honorary_date_from is not None and self.date_from is None:
            raise ValidationError("Cannot have a 'honorary from date' without a 'date from'. (Honorary member must be a"
                                  " regular member too)")

        if self.date_to is None and self.associate_member:
            raise ValidationError(
                "'Date to' is required for associate members")

        if self.date_to is None and self.donating_member:
            raise ValidationError("'Date to' is required for donating members")
