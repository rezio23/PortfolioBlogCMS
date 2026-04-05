from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsViewsTests(TestCase):
    def test_register_page_returns_success(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_returns_success(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continue with Gmail")
        self.assertContains(response, "Continue with GitHub")
        self.assertContains(response, "Continue with Facebook")

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        user = get_user_model().objects.create_user(username="writer", password="safe-pass-123")

        response = self.client.post(
            reverse("login"),
            {
                "username": user.username,
                "password": "safe-pass-123",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"), fetch_redirect_response=False)

    def test_unconfigured_social_shortcut_redirects_back_to_login(self):
        response = self.client.get(reverse("social-login-shortcut", args=["google"]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gmail sign-in is not configured yet")
