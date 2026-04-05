from urllib.parse import urlparse

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.core.models import SiteConfiguration

from .forms import ContactForm


def _format_profile_value(url):
    if not url:
        return "Add this link in Site Configuration"

    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path = parsed.path.rstrip("/")

    if host and path:
        return f"{host}{path}"
    if host:
        return host
    return url


def _build_contact_channels(config):
    contact_email = getattr(config, "contact_email", "") or ""
    facebook_url = getattr(config, "facebook_url", "") or ""
    instagram_url = getattr(config, "instagram_url", "") or ""
    tiktok_url = getattr(config, "tiktok_url", "") or ""
    github_url = getattr(config, "github_url", "") or ""

    return [
        {
            "key": "email",
            "title": "Email",
            "icon": "fa-solid fa-envelope",
            "value": contact_email or "Add your email in Site Configuration",
            "hint": "Best for project details, questions, and direct collaboration.",
            "url": f"mailto:{contact_email}" if contact_email else "",
            "cta": "Send email" if contact_email else "Not configured",
            "new_tab": False,
        },
        {
            "key": "facebook",
            "title": "Facebook",
            "icon": "fa-brands fa-facebook-f",
            "value": _format_profile_value(facebook_url),
            "hint": "Stay connected through updates, messages, and community-friendly sharing.",
            "url": facebook_url,
            "cta": "Open profile" if facebook_url else "Not configured",
            "new_tab": True,
        },
        {
            "key": "instagram",
            "title": "Instagram",
            "icon": "fa-brands fa-instagram",
            "value": _format_profile_value(instagram_url),
            "hint": "A better place for visual moments, design snapshots, and creative progress.",
            "url": instagram_url,
            "cta": "View account" if instagram_url else "Not configured",
            "new_tab": True,
        },
        {
            "key": "tiktok",
            "title": "TikTok",
            "icon": "fa-brands fa-tiktok",
            "value": _format_profile_value(tiktok_url),
            "hint": "Short-form updates, experiments, and behind-the-scenes content.",
            "url": tiktok_url,
            "cta": "Watch content" if tiktok_url else "Not configured",
            "new_tab": True,
        },
        {
            "key": "github",
            "title": "GitHub",
            "icon": "fa-brands fa-github",
            "value": _format_profile_value(github_url),
            "hint": "Browse repositories, commit history, and the code behind the work.",
            "url": github_url,
            "cta": "View projects" if github_url else "Not configured",
            "new_tab": True,
        },
    ]


def contact_view(request):
    config = SiteConfiguration.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out. Your message has been sent.")
            return redirect("contact:contact_success")
    else:
        form = ContactForm()

    context = {
        "form": form,
        "contact_channels": _build_contact_channels(config),
    }
    return render(request, "contact/contact.html", context)


def contact_success_view(request):
    return render(request, "contact/contact_success.html")
