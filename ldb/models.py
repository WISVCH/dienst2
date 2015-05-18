# -*- coding: utf-8 -*-
from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from country_field import CountryField
from dienst2.extras import CharNullField


def get_attributes(self, attrs):
    v = {}
    for attr in attrs:
        v[self._meta.get_field(attr).verbose_name] = self.__getattribute__(attr)
    return v


class Entity(models.Model):
    class Meta:
        verbose_name = _('entity')
        verbose_name_plural = _('entities')

    # Adress
    street_name = models.CharField(_('street name'), max_length=75, blank=True)
    house_number = models.CharField(_('house number'), max_length=7, blank=True)
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
    constitution_card = models.BooleanField(_('constitution card'), default=False)
    christmas_card = models.BooleanField(_('Christmas card'), default=True)
    yearbook = models.BooleanField(_('yearbook'), default=False)

    # Other
    comment = models.TextField(blank=True)

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

    def __unicode__(self):
        return u'%s %s, %s %s, %s' % (self.street_name, self.house_number,
                                      self.postcode, self.city, self.country)

    def set_address_incorrect(self):
        self.street_name = ''
        self.house_number = ''
        self.address_2 = ''
        self.address_3 = ''
        self.postcode = ''
        self.city = ''
        self.country = ''


class Organization(Entity):
    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    name_prefix = models.CharField(_('name prefix'), max_length=100)
    name = models.CharField(_('name'), max_length=100)
    name_short = models.CharField(_('name short'), max_length=100, blank=True)
    salutation = models.CharField(_('salutation'), max_length=100)

    @models.permalink
    def get_absolute_url(self):
        return ('ldb_organizations_detail', [str(self.id)])

    def __unicode__(self):
        return unicode(self.name)


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
    preposition = models.CharField(_('preposition'), max_length=15, blank=True)  # Tussenvoegsel
    surname = models.CharField(_('surname'), max_length=100)
    postfix_titles = models.CharField(_('postfix titles'), max_length=20, blank=True)

    # Telephone
    phone_mobile = models.CharField(_('phone mobile'), max_length=16, blank=True)

    # Other
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)

    deceased = models.BooleanField(_('deceased'), default=False)
    # https://code.djangoproject.com/ticket/7689
    # _living_with     =models.ManyToManyField('self')
    living_with = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL)

    # Subscriptions
    mail_announcements = models.BooleanField(_('announcements mailing'), default=True)
    mail_company = models.BooleanField(_('company mailing'), default=True)

    ldap_username = CharNullField(_('LDAP username'), max_length=64, blank=True, null=True, unique=True)

    # External Accounts
    netid = CharNullField(_('NetID'), max_length=64, blank=True, null=True, unique=True)
    linkedin_id = CharNullField(_('LinkedIn ID'), max_length=64, blank=True, null=True, unique=True)
    facebook_id = CharNullField(_('Facebook ID'), max_length=64, blank=True, null=True, unique=True)

    __original_living_with_id = None

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.__original_living_with_id = self.living_with_id

    @property
    def subscriptions(self):
        return get_attributes(self, ['machazine', 'constitution_card',
                                     'christmas_card', 'board_invites',
                                     'mail_announcements', 'mail_company'])

    @property
    def gender_symbol(self):
        if self.gender == 'M':
            return u'♂'
        elif self.gender == 'F':
            return u'♀'
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

    def save(self):
        super(Person, self).save()
        if self.pk is not None:
            old = self.__original_living_with_id
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

    @models.permalink
    def get_absolute_url(self):
        return ('ldb_people_detail', [str(self.id)])

    def __unicode__(self):
        return (u'%s, %s %s%s' % \
                (self.surname, self.firstname, self.preposition, u' ✝' if self.deceased else '')).strip()


class Member(models.Model):
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    person = models.OneToOneField(Person, primary_key=True)

    date_from = models.DateField(_('date from'), blank=True, null=True)
    date_to = models.DateField(_('date to'), blank=True, null=True)
    date_paid = models.DateField(_('date paid'), blank=True, null=True)
    amount_paid = models.IntegerField(_('amount paid'), blank=True, null=True)

    associate_member = models.BooleanField(_('associate member'), default=False)
    donating_member = models.BooleanField(_('donating member'), default=False)

    merit_date_from = models.DateField(_('merit member date from'), blank=True, null=True)
    merit_invitations = models.BooleanField(_('merit member invitations'), default=True)
    merit_history = models.TextField(_('merit member history'), blank=True)

    honorary_date_from = models.DateField(_('honorary member from date'), blank=True, null=True)

    @property
    def current_member(self):
        return (self.date_from is not None and self.date_to is None) or \
               self.merit_date_from is not None or self.honorary_date_from is not None

    def __unicode__(self):
        return unicode(self.person)

    def clean(self):
        if (self.date_from is not None and self.date_to is not None and self.date_from > self.date_to) or \
                (self.date_to is not None and self.date_to is None):
            raise ValidationError("'Date to' cannot be before 'date from'")


class Student(models.Model):
    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    person = models.OneToOneField(Person, primary_key=True)

    study = models.CharField(_('study'), max_length=50)
    first_year = models.IntegerField(_('first year'), blank=True, null=True)
    student_number = CharNullField(_('student number'), max_length=7, blank=True, null=True, unique=True)
    graduated = models.BooleanField(_('graduated'), default=False)

    phone_parents = models.CharField(_('phone parents'), max_length=16, blank=True)

    yearbook_permission = models.BooleanField(_('yearbook permission'), default=True)

    date_verified = models.DateField(_('date verified'), blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.student_number, unicode(self.person))


CONTACT_METHOD_CHOICES = (
    ('m', 'Mail'),
    ('e', 'Email'),
)


class Alumnus(models.Model):
    class Meta:
        verbose_name = _('alumnus')
        verbose_name_plural = _('alumni')

    person = models.OneToOneField(Person, primary_key=True)

    study = models.CharField(_('study'), max_length=100, blank=True)
    study_first_year = models.IntegerField(_('study first year'), blank=True, null=True)
    study_last_year = models.IntegerField(_('study last year'), blank=True, null=True)
    study_research_group = models.CharField(_('research group'), max_length=100, blank=True)
    study_paper = models.CharField(_('paper'), max_length=300, blank=True)
    study_professor = models.CharField(_('professor'), max_length=100, blank=True)

    work_company = models.CharField(_('company'), max_length=100, blank=True)
    work_position = models.CharField(_('position'), max_length=100, blank=True)
    work_sector = models.CharField(_('sector'), max_length=100, blank=True)

    contact_method = models.CharField(_('contact method'), max_length=1, choices=CONTACT_METHOD_CHOICES, default='e')

    def __unicode__(self):
        return unicode(self.person)


class Employee(models.Model):
    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    person = models.OneToOneField(Person, primary_key=True)

    faculty = models.CharField(_('faculty'), max_length=50)
    department = models.CharField(_('department'), max_length=50)
    function = models.CharField(_('function'), max_length=50)
    phone_internal = models.CharField(_('phone internal'), max_length=5)

    def __unicode__(self):
        return unicode(self.person)


class Committee(models.Model):
    class Meta:
        verbose_name = _('committee')
        verbose_name_plural = _('committees')

    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    members = models.ManyToManyField(Person, through='CommitteeMembership')

    def __unicode__(self):
        return self.name


class CommitteeMembership(models.Model):
    class Meta:
        verbose_name = _('committee membership')
        verbose_name_plural = _('committee memberships')

    # Django admin doesn't support nested inlines,
    # so we'll just link to Person instead.
    person = models.ForeignKey(Person, related_name="committee_memberships")
    committee = models.ForeignKey(Committee)
    board = models.IntegerField(_('board'))
    position = models.CharField(_('position'), max_length=50, blank=True)
    ras_months = models.IntegerField(_('RAS months'), blank=True, null=True)

    def __unicode__(self):
        return u'[%s] %s - %s' % (self.board, self.committee, self.person)


class Modification(models.Model):
    class Meta:
        verbose_name = _('modification')
        verbose_name_plural = _('modifications')

    person = models.ForeignKey(Person)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    ip = models.CharField(_('ip address'), max_length=40)
    modification = models.TextField(_('modification'), blank=True)

    def __unicode__(self):
        return u'Edit [%s] %s' % (self.date, self.person.__unicode__())
