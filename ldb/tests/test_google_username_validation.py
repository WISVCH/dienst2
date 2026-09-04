from django.core.exceptions import ValidationError
from django.test import TestCase

from ldb.admin import PersonAdminForm
from ldb.tests.helpers import LDBHelperMixin


class GoogleUsernameValidationTestCase(LDBHelperMixin, TestCase):
    def test_invalid_google_username_is_rejected_before_saving(self):
        person = self.create_person(initials="J.", firstname="Jane", surname="Doe")
        person.google_username = "jane.doe@example.com"

        with self.assertRaises(ValidationError):
            person.save()

        person.refresh_from_db()
        self.assertIsNone(person.google_username)

    def test_invalid_google_username_is_shown_on_admin_form(self):
        form = PersonAdminForm(
            data={
                "initials": "J.",
                "firstname": "Jane",
                "surname": "Doe",
                "google_username": "jane.doe@example.com",
                "_membership_status": "0",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("google_username", form.errors)
