from django.core.exceptions import ValidationError
from django.test import TestCase

from ldb.models import Student, MembershipStatus
from ldb.tests.helpers import LDBHelperMixin


class MembershipStatusTestCase(LDBHelperMixin, TestCase):
    def test_deceased(self):
        person = self.create_current_member(
            person_kwargs={'deceased': True},
        )
        member = self.get_member(person.pk)
        self.assertFalse(member.current_member, 'deceased=True')

    def test_date_to_yesterday(self):
        person = self.create_current_member(
            member_kwargs={'date_to': self.yesterday},
        )
        member = self.get_member(person.pk)
        self.assertFalse(member.current_member, 'member.date_to=yesterday')

    def test_date_to_tomorrow(self):
        person = self.create_current_member(
            member_kwargs={'date_to': self.tomorrow},
        )
        member = self.get_member(person.pk)
        self.assertTrue(member.current_member, 'member.date_to=yesterday')

    def test_donating_member(self):
        person = self.create_donating_member()
        self.assertEqual(person.membership_status, MembershipStatus.DONATING, 'donating member')

    def test_donating_member_no_date_to(self):
        person = self.create_associate_member()

        person.member.date_to = None
        self.assertRaises(ValidationError, person.member.full_clean)

    def test_alumnus_member(self):
        person = self.create_alumnus_member()
        self.assertEqual(person.membership_status, MembershipStatus.ALUMNUS)

    def test_alumnus_member_with_student(self):
        person = self.create_alumnus_member()

        person.student = Student.objects.create(person=person, enrolled=True)
        person.save()

        person = self.get_person(person.pk)
        self.assertNotEqual(person.membership_status, MembershipStatus.ALUMNUS)

        person.student.enrolled = False
        person.student.save()

        person = self.get_person(person.pk)
        self.assertEqual(person.membership_status, MembershipStatus.ALUMNUS)

    def test_regular_member(self):
        person = self.create_regular_member()
        self.assertEqual(person.membership_status, MembershipStatus.REGULAR, 'regular member')

    def test_no_longer_student(self):
        person = self.create_regular_member(
            student_kwargs={'enrolled': False},
        )
        self.assertEqual(person.membership_status, MembershipStatus.NONE, 'student.enrolled=False')

    def test_associate_member(self):
        person = self.create_associate_member()
        self.assertEqual(person.membership_status, MembershipStatus.ASSOCIATE, 'associate member')

    def test_associate_member_no_date_to(self):
        person = self.create_associate_member()

        person.member.date_to = None
        self.assertRaises(ValidationError, person.member.full_clean)

    def test_merit_member(self):
        person = self.create_merit_member()
        self.assertEqual(person.membership_status, MembershipStatus.MERIT, 'default merit member')

    def test_merit_member_date_from_in_future(self):
        person = self.create_merit_member()

        person.member.merit_date_from = self.tomorrow
        self.assertRaises(ValidationError, person.member.full_clean)

    def test_honorary_member(self):
        person = self.create_honorary_member()
        self.assertEqual(person.membership_status, MembershipStatus.HONORARY, 'honorary member')

    def test_honorary_member_date_from_in_future(self):
        person = self.create_honorary_member()

        person.member.honorary_date_from = self.tomorrow
        self.assertRaises(ValidationError, person.member.full_clean)
