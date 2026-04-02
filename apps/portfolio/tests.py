from django.test import TestCase
from django.urls import reverse


class PortfolioViewsTests(TestCase):
    def test_project_list_returns_success(self):
        response = self.client.get(reverse("portfolio:project_list"))
        self.assertEqual(response.status_code, 200)
