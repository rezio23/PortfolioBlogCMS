from django.contrib import admin

from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "updated_at")
    search_fields = ("site_name", "contact_email")
    fieldsets = (
        ("Site Identity", {"fields": ("site_name", "tagline", "about_text")}),
        (
            "Contact Channels",
            {
                "fields": (
                    "contact_email",
                    "education_telegram_group_url",
                    "facebook_url",
                    "instagram_url",
                    "tiktok_url",
                    "youtube_url",
                    "x_url",
                    "threads_url",
                    "github_url",
                )
            },
        ),
    )
