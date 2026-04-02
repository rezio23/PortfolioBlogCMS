from .models import SiteConfiguration


def site_meta(request):
    config = SiteConfiguration.objects.first()
    if not config:
        return {
            "site_name": "Portfolio Blog CMS",
            "site_tagline": "Showcase your work and publish your ideas.",
            "site_about": "A starter portfolio and blog platform built with Django.",
        }

    return {
        "site_name": config.site_name,
        "site_tagline": config.tagline,
        "site_about": config.about_text,
    }
