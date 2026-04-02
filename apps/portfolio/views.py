from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


PROJECTS_PER_PAGE = 6


def project_list(request):
    paginator = Paginator(Project.objects.all(), PROJECTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "portfolio/project_list.html", {"page_obj": page_obj, "projects": page_obj.object_list})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project created successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm()
    return render(request, "portfolio/project_create.html", {"form": form})


@login_required
def project_update(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect(project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)

    return render(request, "portfolio/project_update.html", {"form": form, "project": project})


@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect("portfolio:project_list")

    return render(request, "portfolio/project_delete.html", {"project": project})
