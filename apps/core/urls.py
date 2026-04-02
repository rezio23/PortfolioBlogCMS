from django.urls import path

from .views import AboutView, HomeView, ServicesView, SkillsView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("skills/", SkillsView.as_view(), name="skills"),
    path("services/", ServicesView.as_view(), name="services"),
]
