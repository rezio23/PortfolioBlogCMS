from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.blog.models import Post

from .forms import ProfileForm, UserLoginForm, UserRegistrationForm, UserUpdateForm


SOCIAL_PROVIDER_META = {
    "google": {
        "label": "Gmail",
        "icon": "fa-brands fa-google",
        "status_ready": "Quick access ready",
        "status_pending": "Setup shortcut",
    },
    "github": {
        "label": "GitHub",
        "icon": "fa-brands fa-github",
        "status_ready": "Quick access ready",
        "status_pending": "Setup shortcut",
    },
    "facebook": {
        "label": "Facebook",
        "icon": "fa-brands fa-facebook-f",
        "status_ready": "Quick access ready",
        "status_pending": "Setup shortcut",
    },
}


def _append_query(url, **params):
    if not url:
        return url

    parsed = urlsplit(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({key: value for key, value in params.items() if value})
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provider_urls = getattr(settings, "SOCIAL_LOGIN_URLS", {})
        next_url = self.request.GET.get(self.redirect_field_name, "")

        social_providers = []
        for key, meta in SOCIAL_PROVIDER_META.items():
            configured = bool(provider_urls.get(key))
            shortcut_url = reverse("social-login-shortcut", args=[key])
            shortcut_url = _append_query(shortcut_url, next=next_url)
            social_providers.append(
                {
                    "key": key,
                    "label": meta["label"],
                    "icon": meta["icon"],
                    "url": shortcut_url,
                    "configured": configured,
                    "status": meta["status_ready"] if configured else meta["status_pending"],
                }
            )

        context["social_providers"] = social_providers
        context["social_shortcuts_ready"] = any(provider["configured"] for provider in social_providers)
        return context


def social_login_shortcut_view(request, provider):
    provider_meta = SOCIAL_PROVIDER_META.get(provider)
    if not provider_meta:
        raise Http404("Unknown social provider")

    provider_urls = getattr(settings, "SOCIAL_LOGIN_URLS", {})
    provider_url = provider_urls.get(provider)
    next_url = request.GET.get("next", "")

    if provider_url:
        return redirect(_append_query(provider_url, next=next_url))

    messages.info(
        request,
        f"{provider_meta['label']} sign-in is not configured yet. Add the provider URL when you are ready to connect it.",
    )
    return redirect(_append_query(reverse("login"), next=next_url))


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now sign in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"profile": request.user.profile})


@login_required
def profile_edit_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/profile_edit.html", context)


@login_required
def dashboard_view(request):
    context = {
        "post_count": Post.objects.filter(author=request.user).count(),
    }
    return render(request, "accounts/dashboard.html", context)
