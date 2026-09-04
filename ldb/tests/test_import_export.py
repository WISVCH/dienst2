from django.test import TestCase
from tablib import Dataset

from ldb.admin import PersonResource
from ldb.tests.helpers import LDBHelperMixin


class PersonResourceTestCase(LDBHelperMixin, TestCase):
    def test_import_updates_person_student_and_member(self):
        person = self.create_regular_member(
            person_kwargs={
                "initials": "A.",
                "firstname": "Ada",
                "surname": "Lovelace",
                "netid": "alovelace",
                "email": "old@example.org",
            },
            member_kwargs={"amount_paid": 10},
            student_kwargs={
                "student_number": "1234567",
                "study": "Computer Science",
                "first_year": 2024,
                "emergency_name": "Old contact",
                "emergency_phone": "0100000000",
            },
        )
        resource = PersonResource()
        exported_dataset = resource.export(person.__class__.objects.filter(pk=person.pk))
        row = list(exported_dataset[0])

        row[exported_dataset.headers.index("email")] = "new@example.org"
        row[exported_dataset.headers.index("student__first_year")] = 2025
        row[exported_dataset.headers.index("student__emergency_name")] = "New contact"
        row[exported_dataset.headers.index("member__amount_paid")] = 25
        dataset = Dataset(headers=exported_dataset.headers)
        dataset.append(row)

        result = resource.import_data(dataset, dry_run=False, raise_errors=True)

        self.assertFalse(result.has_errors())
        person.refresh_from_db()
        self.assertEqual(person.email, "new@example.org")
        self.assertEqual(person.student.first_year, 2025)
        self.assertEqual(person.student.emergency_name, "New contact")
        self.assertEqual(person.member.amount_paid, 25)

    def test_import_rejects_invalid_person_without_saving(self):
        person = self.create_regular_member(
            person_kwargs={
                "initials": "A.",
                "firstname": "Ada",
                "surname": "Lovelace",
                "netid": "alovelace",
            },
            student_kwargs={
                "student_number": "1234567",
                "study": "Computer Science",
            },
        )
        resource = PersonResource()
        exported_dataset = resource.export(person.__class__.objects.filter(pk=person.pk))
        row = list(exported_dataset[0])

        row[exported_dataset.headers.index("id")] = 999999
        row[exported_dataset.headers.index("netid")] = "invalid-person"
        row[exported_dataset.headers.index("student__student_number")] = "7654321"
        row[exported_dataset.headers.index("student__study")] = ""
        dataset = Dataset(headers=exported_dataset.headers)
        dataset.append(row)

        result = resource.import_data(dataset, dry_run=False)

        self.assertTrue(result.has_validation_errors())
        self.assertFalse(person.__class__.objects.filter(netid="invalid-person").exists())
