from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class PortfolioView(TemplateView):
    template_name = "core/portfolio.html"


class SkillsView(PortfolioView):
    pass


class ServicesView(TemplateView):
    template_name = "core/services.html"


def error_403(request, exception):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
