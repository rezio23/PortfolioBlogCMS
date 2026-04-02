from django.urls import path

from .views import dashboard_view, profile_edit_view, profile_view, register_view

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
