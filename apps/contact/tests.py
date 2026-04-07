from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from apps.core.models import SiteConfiguration

from .models import ContactMessage


class ContactViewsTests(TestCase):
    def test_contact_page_returns_success(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_shows_all_channels_with_dynamic_display_text(self):
        config = SiteConfiguration.objects.first() or SiteConfiguration.objects.create()
        config.contact_email = "hello@example.com"
        config.education_telegram_group_url = "https://t.me/education_group"
        config.facebook_url = ""
        config.instagram_url = ""
        config.tiktok_url = ""
        config.youtube_url = "https://youtube.com/@blogcms"
        config.x_url = "https://x.com/blogcms?s=21"
        config.threads_url = ""
        config.github_url = ""
        config.save()

        response = self.client.get(reverse("contact:contact"))
        channels = response.context["contact_channels"]

        self.assertEqual(len(channels), 9)
        self.assertEqual(channels[0]["value"], "hello@example.com")
        self.assertEqual(channels[1]["value"], "t.me/education_group")
        self.assertEqual(channels[5]["value"], "youtube.com/@blogcms")
        self.assertEqual(channels[6]["value"], "x.com/blogcms")
        self.assertEqual(channels[2]["value"], "Add your Facebook link in Site Configuration")
        self.assertEqual(channels[7]["value"], "Add your Threads profile link in Site Configuration")
        self.assertContains(response, "Add your Facebook link in Site Configuration")
        self.assertContains(response, "Add your Threads profile link in Site Configuration")
        self.assertContains(response, "t.me/education_group")
        self.assertNotContains(response, "No live channels yet")

    @patch("apps.contact.views.send_contact_message_to_telegram")
    def test_contact_submission_saves_message_and_sends_telegram_notification(self, send_contact_message):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "subject": "New project",
                "message": "I would like to work with you.",
            },
        )

        self.assertRedirects(response, reverse("contact:contact_success"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        send_contact_message.assert_called_once_with(ContactMessage.objects.get())

    @patch("apps.contact.views.send_contact_message_to_telegram")
    def test_contact_submission_requires_all_fields(self, send_contact_message):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "",
                "email": "",
                "subject": "",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "Please enter your name.")
        self.assertFormError(response.context["form"], "email", "Please enter your email address.")
        self.assertFormError(response.context["form"], "subject", "Please enter a subject.")
        self.assertFormError(response.context["form"], "message", "Please enter your message.")
        self.assertEqual(ContactMessage.objects.count(), 0)
        send_contact_message.assert_not_called()

    @patch("apps.contact.views.send_contact_message_to_telegram")
    def test_contact_submission_rejects_name_with_numbers(self, send_contact_message):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "Jane123",
                "email": "jane@example.com",
                "subject": "New project",
                "message": "I would like to work with you.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "Name cannot contain numbers.")
        self.assertEqual(ContactMessage.objects.count(), 0)
        send_contact_message.assert_not_called()

    @patch("apps.contact.views.send_contact_message_to_telegram")
    def test_contact_submission_rejects_uppercase_email(self, send_contact_message):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "Jane Doe",
                "email": "Jane@Example.com",
                "subject": "New project",
                "message": "I would like to work with you.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "Email must use lowercase letters only.")
        self.assertEqual(ContactMessage.objects.count(), 0)
        send_contact_message.assert_not_called()
