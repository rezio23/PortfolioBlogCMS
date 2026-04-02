from django.urls import path

from .views import contact_success_view, contact_view

app_name = "contact"

urlpatterns = [
    path("", contact_view, name="contact"),
    path("success/", contact_success_view, name="contact_success"),
]
