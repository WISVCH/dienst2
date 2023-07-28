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
