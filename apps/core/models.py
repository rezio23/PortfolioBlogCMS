from django.db import models


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Portfolio Blog CMS")
    tagline = models.CharField(max_length=255, blank=True)
    about_text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name
