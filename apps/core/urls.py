from django.urls import path

from .views import AboutView, HomeView, PortfolioView, ServicesView, SkillsView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("skills/", SkillsView.as_view(), name="skills"),
    path("services/", ServicesView.as_view(), name="services"),
]
