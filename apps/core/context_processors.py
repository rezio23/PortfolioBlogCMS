from .models import SiteConfiguration


def site_meta(request):
    config = SiteConfiguration.objects.first()
    if not config:
        return {
            "site_name": "Blog CMS",
            "site_tagline": "Publish your ideas and manage your content.",
            "site_about": "A starter blog platform built with Django.",
        }

    return {
        "site_name": config.site_name,
        "site_tagline": config.tagline,
        "site_about": config.about_text,
    }