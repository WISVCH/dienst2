from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ldb.tests.helpers import LDBHelperMixin


class ApiV3TestCase(LDBHelperMixin, APITestCase):
    def setUp(self):
        self.user = User.objects.create()

        self.GOOGLE_USERNAME = "google"

        self.create_person(google_username=self.GOOGLE_USERNAME)
        self.create_person()
        self.create_person()

    def login_with_token(self):
        key = "welcome"
        token = Token.objects.create(key=key, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_token_authentication(self):
        self.login_with_token()

        url = reverse("person-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_authentication_fail(self):
        url = reverse("person-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_person_list(self):
        self.login_with_token()
        url = reverse("person-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_person_filter_exists(self):
        self.login_with_token()
        url = reverse("person-list")
        response = self.client.get(url, {"google_username": self.GOOGLE_USERNAME})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_person_filter_not_exists(self):
        self.login_with_token()
        url = reverse("person-list")
        response = self.client.get(url, {"google_username": "does not exist"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_person_update(self):
        self.login_with_token()
        person = self.create_person(initials="J.", firstname="Jane", surname="Doe")

        response = self.client.patch(
            reverse("person-detail", args=[person.pk]),
            {
                "initials": person.initials,
                "firstname": person.firstname,
                "surname": person.surname,
                "pronouns": "they/them",
                "email": "jane.doe@example.com",
                "phone_mobile": "+31612345678",
                "street_name": "Mekelweg",
                "house_number": "4",
                "postcode": "2628 CD",
                "city": "Delft",
                "country": "NL",
                "machazine": False,
                "mail_announcements": False,
                "mail_company": True,
                "mail_education": True,
                "revision_comment": "Updated by Jane Doe via the website.",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "jane.doe@example.com")
        self.assertEqual(response.data["phone_mobile"], "+31612345678")
        self.assertEqual(response.data["city"], "Delft")
        self.assertFalse(response.data["machazine"])
        self.assertFalse(response.data["mail_announcements"])
        self.assertTrue(response.data["mail_company"])
        self.assertTrue(response.data["mail_education"])

        person.refresh_from_db()
        self.assertEqual(person.pronouns, "they/them")
        self.assertEqual(person.street_name, "Mekelweg")
        self.assertEqual(person.country, "NL")
