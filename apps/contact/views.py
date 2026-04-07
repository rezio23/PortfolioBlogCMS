from urllib.parse import urlparse

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.core.models import SiteConfiguration

from .forms import ContactForm
from .services import send_contact_message_to_telegram


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


def _build_channel(*, key, title, icon, value, url, configured_cta, empty_value, empty_cta="Add link", new_tab=True):
    is_configured = bool(url)
    return {
        "key": key,
        "title": title,
        "icon": icon,
        "value": value if is_configured else empty_value,
        "url": url,
        "cta": configured_cta if is_configured else empty_cta,
        "new_tab": new_tab,
    }


def _build_contact_channels(config):
    contact_email = getattr(config, "contact_email", "") or ""
    education_telegram_group_url = getattr(config, "education_telegram_group_url", "") or ""
    facebook_url = getattr(config, "facebook_url", "") or ""
    instagram_url = getattr(config, "instagram_url", "") or ""
    tiktok_url = getattr(config, "tiktok_url", "") or ""
    youtube_url = getattr(config, "youtube_url", "") or ""
    x_url = getattr(config, "x_url", "") or ""
    threads_url = getattr(config, "threads_url", "") or ""
    github_url = getattr(config, "github_url", "") or ""

    return [
        _build_channel(
            key="email",
            title="Email",
            icon="fa-solid fa-envelope",
            value=contact_email,
            url=f"mailto:{contact_email}" if contact_email else "",
            configured_cta="Send email",
            empty_value="Add your email in Site Configuration",
            empty_cta="Add email",
            new_tab=False,
        ),
        _build_channel(
            key="education-telegram",
            title="12 Exam Preparation",
            icon="fa-brands fa-telegram",
            value=_format_profile_value("Education Telegram Group"),
            url="https://t.me/sombath12examfiles",
            configured_cta="Join group",
            empty_value="Add your Telegram group link in Site Configuration",
        ),
        _build_channel(
            key="facebook",
            title="Vichhean Som Bath",
            icon="fa-brands fa-facebook-f",
            value=_format_profile_value("Facebook Profile"),
            url="https://www.facebook.com/v.bathhh/",
            configured_cta="Open profile",
            empty_value="Add your Facebook link in Site Configuration",
        ),
        _build_channel(
            key="instagram",
            title="23Rezio",
            icon="fa-brands fa-instagram",
            value=_format_profile_value("Instagram Profile"),
            url="https://www.instagram.com/rezio_23?igsh=bDMyOGtqdTBsY3Vj&utm_source=qr",
            configured_cta="View profile",
            empty_value="Add your Instagram link in Site Configuration",
        ),
        _build_channel(
            key="tiktok",
            title="Rezio",
            icon="fa-brands fa-tiktok",
            value=_format_profile_value("Tiktok Profile"),
            url="https://www.tiktok.com/@reziooo23?_r=1&_t=ZS-95Bsuz7gpa4",
            configured_cta="Open profile",
            empty_value="Add your TikTok link in Site Configuration",
        ),
        _build_channel(
            key="youtube",
            title="YouTube",
            icon="fa-brands fa-youtube",
            value=_format_profile_value(youtube_url),
            url=youtube_url,
            configured_cta="Watch channel",
            empty_value="Add your YouTube channel link in Site Configuration",
        ),
        _build_channel(
            key="x",
            title="R3zio",
            icon="fa-brands fa-x-twitter",
            value=_format_profile_value("X Profile"),
            url="https://x.com/rezio_23?s=21",
            configured_cta="View profile",
            empty_value="Add your X profile link in Site Configuration",
        ),
        _build_channel(
            key="threads",
            title="23Rezio",
            icon="fa-brands fa-threads",
            value=_format_profile_value("Thread Profile"),
            url="https://www.threads.com/@rezio_23?igshid=NTc4MTIwNjQ2YQ==",
            configured_cta="View profile",
            empty_value="Add your Threads profile link in Site Configuration",
        ),
        _build_channel(
            key="github",
            title="R3zio",
            icon="fa-brands fa-github",
            value=_format_profile_value("Github Profile"),
            url="https://github.com/rezio23",
            configured_cta="View profile",
            empty_value="Add your GitHub link in Site Configuration",
        ),
    ]


def contact_view(request):
    config = SiteConfiguration.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            send_contact_message_to_telegram(contact_message)
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
