# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from ldb.querysets import EntityQuerySet, PersonQuerySet
from .country_field import CountryField
from .validators import validate_ldap_username


def get_attributes(self, attrs):
    v = {}
    for attr in attrs:
        v[self._meta.get_field(attr).verbose_name] = self.__getattribute__(attr)
    return v


@python_2_unicode_compatible
class Entity(models.Model):
    class Meta:
        verbose_name = _("entity")
        verbose_name_plural = _("entities")

    # Address
    street_name = models.CharField(_("street name"), max_length=75, blank=True)
    house_number = models.CharField(_("house number"), max_length=7, blank=True)
    address_2 = models.CharField(_("address row 2"), max_length=75, blank=True)
    address_3 = models.CharField(_("address row 3"), max_length=75, blank=True)
    postcode = models.CharField(_("postcode"), max_length=10, blank=True)
    city = models.CharField(_("city"), max_length=50, blank=True)
    country = CountryField(_("country"), blank=True)
    email = models.EmailField(_("e-mail"), blank=True)

    # Telephone
    phone_fixed = models.CharField(_("phone fixed"), max_length=16, blank=True)

    # Subscriptions
    machazine = models.BooleanField(_("MaCHazine"), default=True)
    board_invites = models.BooleanField(_("board invites"), default=False)
    constitution_card = models.BooleanField(_("constitution card"), default=False)
    christmas_card = models.BooleanField(_("Christmas card"), default=True)
    yearbook = models.BooleanField(_("yearbook"), default=False)

    # Other
    comment = models.TextField(blank=True)

    objects = EntityQuerySet.as_manager()

    @property
    def street_address(self):
        strings = [
            self.street_name + " " + self.house_number,
            self.address_2,
            self.address_3,
        ]
        return "\n".join(filter(None, strings))

    @property
    def formatted_address(self):
        strings = [
            self.street_address,
            self.postcode
            + ("  " + self.city.upper() if self.postcode != "INTERN" else ""),
            self.get_country_display() if self.country != "NL" else "",
        ]
        return "\n".join(filter(None, strings))

    @property
    def subscriptions(self):
        return get_attributes(
            self,
            [
                "machazine",
                "board_invites",
                "constitution_card",
                "christmas_card",
                "yearbook",
            ],
        )

    def clean(self):
        if (
            self.street_name != ""
            or self.house_number != ""
            or self.address_2 != ""
            or self.address_3 != ""
            or self.postcode != ""
            or self.city != ""
        ) and self.country == "":
            raise ValidationError("Country is required if address is entered.")

    def __str__(self):
        return "%s %s, %s %s, %s" % (
            self.street_name,
            self.house_number,
            self.postcode,
            self.city,
            self.country,
        )

    def set_address_incorrect(self):
        self.street_name = ""
        self.house_number = ""
        self.address_2 = ""
        self.address_3 = ""
        self.postcode = ""
        self.city = ""
        self.country = ""


@python_2_unicode_compatible
class Organization(Entity):
    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        manager_inheritance_from_future = True

    name_prefix = models.CharField(_("name prefix"), max_length=100, blank=True)
    name = models.CharField(_("name"), max_length=100)
    name_short = models.CharField(_("name short"), max_length=100, blank=True)
    salutation = models.CharField(_("salutation"), max_length=100)

    def get_absolute_url(self):
        return reverse("ldb_organizations_detail", args=[str(self.id)])

    def __str__(self):
        return str(self.name)


class MembershipStatus(object):
    NONE = 0
    DONATING = 10
    ALUMNUS = 20
    REGULAR = 30
    ASSOCIATE = 40
    MERIT = 50
    HONORARY = 60

    labels = {
        NONE: _("Not a member"),
        DONATING: _("Donating member"),
        ALUMNUS: _("Alumnus member"),
        REGULAR: _("Regular member"),
        ASSOCIATE: _("Associate member"),
        MERIT: _("Merit member"),
        HONORARY: _("Honorary member"),
    }

    @classmethod
    def choices(cls):
        return [(value, label) for value, label in cls.labels.items()]


class MembershipStatusField(models.IntegerField):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        kwargs["choices"] = self.enum.choices()
        super(MembershipStatusField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MembershipStatusField, self).deconstruct()
        if self.enum is not None:
            kwargs["enum"] = self.enum
        if "choices" in kwargs:
            del kwargs["choices"]
        return name, path, args, kwargs


@python_2_unicode_compatible
class Person(Entity):
    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    GENDER_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
        ("NB", _("Non-binary")),
        ("O", _("Other")),
    )

    # Name
    titles = models.CharField(_("titles"), max_length=20, blank=True)
    initials = models.CharField(_("initials"), max_length=15)
    firstname = models.CharField(_("first name"), max_length=50)
    preposition = models.CharField(
        _("preposition"), max_length=15, blank=True
    )  # Tussenvoegsel
    surname = models.CharField(_("surname"), max_length=100)
    postfix_titles = models.CharField(_("postfix titles"), max_length=20, blank=True)

    # Telephone
    phone_mobile = models.CharField(_("phone mobile"), max_length=16, blank=True)

    # Other
    gender = models.CharField(
        _("gender"), max_length=2, choices=GENDER_CHOICES, blank=True
    )

    pronouns = models.CharField(_("pronouns"), max_length=100, blank=True)

    birthdate = models.DateField(_("birthdate"), blank=True, null=True)

    deceased = models.BooleanField(_("deceased"), default=False)
    # https://code.djangoproject.com/ticket/7689
    # _living_with     =models.ManyToManyField('self')
    living_with = models.OneToOneField(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )

    # Subscriptions
    mail_announcements = models.BooleanField(_("announcements mailing"), default=True)
    mail_company = models.BooleanField(_("company mailing"), default=True)
    mail_education = models.BooleanField(_("education mailing"), default=True)

    # Internal Account
    ldap_username = models.CharField(
        _("LDAP username"),
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_ldap_username],
    )
    email_forward = models.BooleanField(
        _("forward CH e-mail to Dienst2 e-mail"), default=False
    )

    # External Accounts
    netid = models.CharField(
        _("NetID"), max_length=64, blank=True, null=True, unique=True
    )
    linkedin_id = models.CharField(
        _("LinkedIn ID"), max_length=64, blank=True, null=True, unique=True
    )
    facebook_id = models.CharField(
        _("Facebook ID"), max_length=64, blank=True, null=True, unique=True
    )

    # Membership status
    _membership_status = MembershipStatusField(
        enum=MembershipStatus,
        db_column="membership_status",
        default=MembershipStatus.NONE,
    )

    _original_living_with_id = None

    objects = PersonQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self._original_living_with_id = self.living_with_id

    @property
    def membership_status(self):
        try:
            member = self.member
        except Member.DoesNotExist:
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
            if (
                member.current_member
                and self.membership_status == MembershipStatus.NONE
            ):
                return False
        except Member.DoesNotExist:
            return True

    @property
    def formatted_name(self):
        strings = [
            self.titles,
            self.initials,
            self.preposition,
            self.surname,
            self.postfix_titles,
        ]
        return " ".join(filter(None, strings))

    @property
    def subscriptions(self):
        return get_attributes(
            self,
            [
                "machazine",
                "constitution_card",
                "christmas_card",
                "board_invites",
                "mail_announcements",
                "mail_company",
                "mail_education",
            ],
        )

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

    def clean(self):
        if self.email_forward:
            if self.ldap_username is None:
                raise ValidationError(
                    {
                        "email_forward": _(
                            "LDAP username must be set to enable forwarding."
                        )
                    }
                )
            if self.email == "":
                raise ValidationError(
                    {"email_forward": _("E-mail must be set to enable forwarding.")}
                )
            if self.email.endswith("ch.tudelft.nl"):
                raise ValidationError(
                    {
                        "email_forward": _(
                            "E-mail cannot be forwarded to a CH e-mail address."
                        )
                    }
                )

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
                if (
                    other.living_with != self
                    or other.street_name != self.street_name
                    or other.house_number != self.house_number
                    or other.address_2 != self.address_2
                    or other.address_3 != self.address_3
                    or other.postcode != self.postcode
                    or other.city != self.city
                    or other.country != self.country
                ):
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
        if hasattr(self, "student"):
            return self.student.student_number
        else:
            return None

    def get_absolute_url(self):
        return reverse("ldb_people_detail", args=[str(self.id)])

    def __str__(self):
        return (
            "%s, %s %s%s"
            % (
                self.surname,
                self.firstname,
                self.preposition,
                " ✝" if self.deceased else "",
            )
        ).strip()


@python_2_unicode_compatible
class Member(models.Model):
    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")

    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)

    date_from = models.DateField(_("date from"), blank=True, null=True)
    date_to = models.DateField(_("date to"), blank=True, null=True)
    date_paid = models.DateField(_("date paid"), blank=True, null=True)
    amount_paid = models.IntegerField(_("amount paid"), blank=True, null=True)

    associate_member = models.BooleanField(_("associate member"), default=False)
    donating_member = models.BooleanField(_("donating member"), default=False)

    merit_date_from = models.DateField(
        _("merit member date from"), blank=True, null=True
    )
    merit_invitations = models.BooleanField(_("merit member invitations"), default=True)
    merit_history = models.TextField(_("merit member history"), blank=True)

    honorary_date_from = models.DateField(
        _("honorary member from date"), blank=True, null=True
    )

    @property
    def current_member(self):
        return (
            self.date_from is not None
            and (self.date_to is None or self.date_to > date.today())
            and not self.person.deceased
        )

    @property
    def current_regular_member(self):
        try:
            student = self.person.student
            return student.enrolled and self.current_member
        except Student.DoesNotExist:
            return False

    @property
    def current_alumnus_member(self):
        return (
            self.current_member
            and Alumnus.objects.filter(person=self.person).exists() > 0
            and not self.current_regular_member
        )

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
        if (
            self.date_from is not None
            and self.date_to is not None
            and self.date_from > self.date_to
        ) or (self.date_to is not None and self.date_from is None):
            raise ValidationError("'Date to' cannot be before 'date from'")

        if self.date_to is not None and (
            self.merit_date_from is not None or self.honorary_date_from is not None
        ):
            raise ValidationError(
                "'Date to' cannot be set for merit and honorary members"
            )

        if self.merit_date_from is not None and self.merit_date_from > date.today():
            raise ValidationError("Merit date from should be in the past")

        if (
            self.honorary_date_from is not None
            and self.honorary_date_from > date.today()
        ):
            raise ValidationError("Honorary date from should be in the past")

        if self.merit_date_from is not None and self.date_from is None:
            raise ValidationError(
                "Cannot have a 'merit from date' without a 'date from'. (Merit member must be a "
                "regular member too)"
            )

        if self.honorary_date_from is not None and self.date_from is None:
            raise ValidationError(
                "Cannot have a 'honorary from date' without a 'date from'. (Honorary member must be a"
                " regular member too)"
            )

        if self.date_to is None and self.associate_member:
            raise ValidationError("'Date to' is required for associate members")

        if self.date_to is None and self.donating_member:
            raise ValidationError("'Date to' is required for donating members")


@python_2_unicode_compatible
class Student(models.Model):
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)

    enrolled = models.BooleanField(_("enrolled"), default=True)
    study = models.CharField(_("study"), max_length=50)
    first_year = models.IntegerField(_("first year"), blank=True, null=True)
    student_number = models.CharField(
        _("student number"), max_length=7, blank=True, null=True, unique=True
    )

    emergency_name = models.CharField(_("emergency name"), max_length=48, blank=True)
    emergency_phone = models.CharField(_("emergency phone"), max_length=16, blank=True)

    yearbook_permission = models.BooleanField(_("yearbook permission"), default=True)

    date_verified = models.DateField(_("date verified"), blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.student_number, str(self.person))


CONTACT_METHOD_CHOICES = (("m", "Mail"), ("e", "Email"))


@python_2_unicode_compatible
class Alumnus(models.Model):
    class Meta:
        verbose_name = _("alumnus")
        verbose_name_plural = _("alumni")

    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)

    study = models.CharField(_("study"), max_length=100, blank=True)
    study_first_year = models.IntegerField(_("study first year"), blank=True, null=True)
    study_last_year = models.IntegerField(_("study last year"), blank=True, null=True)
    study_research_group = models.CharField(
        _("research group"), max_length=100, blank=True
    )
    study_paper = models.CharField(_("paper"), max_length=300, blank=True)
    study_professor = models.CharField(_("professor"), max_length=100, blank=True)

    work_company = models.CharField(_("company"), max_length=100, blank=True)
    work_position = models.CharField(_("position"), max_length=100, blank=True)
    work_sector = models.CharField(_("sector"), max_length=100, blank=True)

    contact_method = models.CharField(
        _("contact method"), max_length=1, choices=CONTACT_METHOD_CHOICES, default="e"
    )

    def __str__(self):
        return str(self.person)


@python_2_unicode_compatible
class Employee(models.Model):
    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    person = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)

    faculty = models.CharField(_("faculty"), max_length=50)
    department = models.CharField(_("department"), max_length=50)
    function = models.CharField(_("function"), max_length=50)
    phone_internal = models.CharField(_("phone internal"), max_length=5)

    def __str__(self):
        return str(self.person)


@python_2_unicode_compatible
class Committee(models.Model):
    class Meta:
        verbose_name = _("committee")
        verbose_name_plural = _("committees")
        ordering = ["name"]

    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    members = models.ManyToManyField(Person, through="CommitteeMembership")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CommitteeMembership(models.Model):
    class Meta:
        verbose_name = _("committee membership")
        verbose_name_plural = _("committee memberships")
        ordering = ["board", "committee__name"]

    # Django admin doesn't support nested inlines,
    # so we'll just link to Person instead.
    person = models.ForeignKey(
        Person, related_name="committee_memberships", on_delete=models.CASCADE
    )
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    board = models.IntegerField(_("board"))
    position = models.CharField(_("position"), max_length=50, blank=True)
    ras_months = models.IntegerField(_("RAS months"), blank=True, null=True)

    def __str__(self):
        return "[%s] %s - %s" % (self.board, self.committee, self.person)


@python_2_unicode_compatible
class Modification(models.Model):
    class Meta:
        verbose_name = _("modification")
        verbose_name_plural = _("modifications")

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    ip = models.CharField(_("ip address"), max_length=40)
    modification = models.TextField(_("modification"), blank=True)

    def __str__(self):
        return "Edit [%s] %s" % (self.date, self.person.__str__())
