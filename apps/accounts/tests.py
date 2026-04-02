from django.test import TestCase
from django.urls import reverse


class AccountsViewsTests(TestCase):
    def test_register_page_returns_success(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
