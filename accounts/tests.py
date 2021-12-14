from django.http import response
from django.test import TestCase
from django.urls import reverse

from . import models

# Create your tests here.


class CustomerTestCase():

    def test_queryset_exists(self):
        qs = models.Customer.objects.all()
        self.assertTrue(qs.exists())


class TestViews(TestCase):
    def test_show_registration(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_show_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_show_reports(self):
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "accounts/reports.html")

    def test_show_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/index.html")

    def test_show_user(self):
        response = self.client.get(reverse('user-page'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "accounts/user.html")

    def test_show_settings(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "accounts/account_settings.html")

    def test_signup_user(self):
        self.user = {
            "first_name": "firstname",
            "last_name": "lastname",
            "username": "username",
            "email": "email",
            "password": "password",
            "password2": "password",
        }

        response = self.client.post(reverse("register"), self.user)
        self.assertEquals(response.status_code, 200)
