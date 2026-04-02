from django.urls import path

from .views import project_create, project_delete, project_detail, project_list, project_update

app_name = "portfolio"

urlpatterns = [
    path("", project_list, name="project_list"),
    path("create/", project_create, name="project_create"),
    path("<slug:slug>/edit/", project_update, name="project_update"),
    path("<slug:slug>/delete/", project_delete, name="project_delete"),
    path("<slug:slug>/", project_detail, name="project_detail"),
]
