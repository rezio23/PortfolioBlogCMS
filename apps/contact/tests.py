from django.test import TestCase
from django.urls import reverse


class ContactViewsTests(TestCase):
    def test_contact_page_returns_success(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)
