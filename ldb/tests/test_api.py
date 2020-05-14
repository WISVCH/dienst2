from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ldb.tests.helpers import LDBHelperMixin


class ApiV3TestCase(LDBHelperMixin, APITestCase):
    def setUp(self):
        self.user = User.objects.create()

        self.LDAP_USERNAME = "ldap"

        self.create_person(ldap_username=self.LDAP_USERNAME)
        self.create_person()
        self.create_person()

    def test_token_authentication(self):
        key = "welcome"
        token = Token.objects.create(key=key, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        url = reverse("person-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_list(self):
        self.client.force_login(self.user)
        url = reverse("person-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_person_filter_exists(self):
        self.client.force_login(self.user)
        url = reverse("person-list")
        response = self.client.get(url, {"ldap_username": self.LDAP_USERNAME})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_person_filter_not_exists(self):
        self.client.force_login(self.user)
        url = reverse("person-list")
        response = self.client.get(url, {"ldap_username": "does not exist"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
