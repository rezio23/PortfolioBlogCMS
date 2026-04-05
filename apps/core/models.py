from django.db import models


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Blog CMS")
    tagline = models.CharField(max_length=255, blank=True)
    about_text = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name
