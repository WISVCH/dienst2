from datetime import timedelta

from django.utils import timezone

from ldb.models import Alumnus, Member, Person, Student

def combine(defaults=None, update_value=None):
    if defaults is None:
        defaults = {}
    if update_value is None:
        update_value = {}

    combined = defaults.copy()
    combined.update(update_value)
    return combined


class LDBHelperMixin(object):
    def setUp(self):
        self.now = timezone.now()
        self.last_week = (self.now - timedelta(weeks=1)).date()
        self.next_week = (self.now + timedelta(weeks=1)).date()
        self.yesterday = (self.now - timedelta(days=1)).date()
        self.tomorrow = (self.now + timedelta(days=1)).date()

    person_defaults = {}

    def create_person(self, **kwargs):
        return Person.objects.create(**combine(self.person_defaults, kwargs))

    def create_current_member(self, person_kwargs=None, member_kwargs=None):
        person = self.create_person(**combine(person_kwargs))

        member_defaults = {
            'person': person,
            'date_from': self.last_week,
        }

        person.member = Member.objects.create(**combine(member_defaults, member_kwargs))
        person.save()

        return self.get_person(person.pk)

    def create_donating_member(self, person_kwargs=None, member_kwargs=None):
        member_defaults = {
            'donating_member': True,
            'date_to': self.next_week
        }

        return self.create_current_member(person_kwargs, combine(member_defaults, member_kwargs))

    def create_alumnus_member(self, person_kwargs=None, member_kwargs=None, alumnus_kwargs=None):
        person = self.create_current_member(person_kwargs, member_kwargs)

        alumnus_defaults = {
            'person': person
        }
        person.alumnus = Alumnus.objects.create(**combine(alumnus_defaults, alumnus_kwargs))
        person.save()

        return person

    def create_regular_member(self, person_kwargs=None, member_kwargs=None, student_kwargs=None):
        person = self.create_current_member(person_kwargs, member_kwargs)

        student_defaults = {
            'person': person,
            'enrolled': True,
        }

        person.student = Student.objects.create(**combine(student_defaults, student_kwargs))
        person.save()

        return person

    def create_associate_member(self, person_kwargs=None, member_kwargs=None):
        member_defaults = {
            'associate_member': True,
            'date_to': self.next_week,
        }

        return self.create_current_member(person_kwargs, combine(member_defaults, member_kwargs))

    def create_merit_member(self, person_kwargs=None, member_kwargs=None):
        member_defaults = {
            'merit_date_from': self.yesterday
        }
        return self.create_current_member(person_kwargs, combine(member_defaults, member_kwargs))

    def create_honorary_member(self, person_kwargs=None, member_kwargs=None):
        member_defaults = {
            'honorary_date_from': self.yesterday
        }
        return self.create_current_member(person_kwargs, combine(member_defaults, member_kwargs))

    def get_person(self, pk):
        return Person.objects.get(pk=pk)

    def get_member(self, pk):
        return Person.objects.get(pk=pk).member
