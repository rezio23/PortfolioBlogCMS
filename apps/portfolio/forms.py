from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "short_description",
            "description",
            "tech_stack",
            "image",
            "project_url",
            "github_url",
            "featured",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            "tech_stack": forms.Textarea(attrs={"rows": 3}),
        }
