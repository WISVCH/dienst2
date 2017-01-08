from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ldb.models import Person


class ApiV3TestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.client.force_login(self.user)

        self.LDAP_USERNAME = 'ldap'
        self.person_1 = Person.objects.create(ldap_username=self.LDAP_USERNAME)
        self.person_2 = Person.objects.create()
        self.person_3 = Person.objects.create()

    def test_person_list(self):
        url = reverse('person-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_person_filter_exists(self):
        url = reverse('person-list')
        response = self.client.get(url, {'ldap_username': self.LDAP_USERNAME})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_person_filter_not_exists(self):
        url = reverse('person-list')
        response = self.client.get(url, {'ldap_username': 'does not exist'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
