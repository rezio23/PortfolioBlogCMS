from django import forms

from .models import Category, Tag


class PostFilterForm(forms.Form):
    title = forms.CharField(required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories",
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label="All tags",
    )

    def filter_queryset(self, queryset):
        title = self.cleaned_data.get("title")
        category = self.cleaned_data.get("category")
        tag = self.cleaned_data.get("tag")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if category:
            queryset = queryset.filter(category=category)
        if tag:
            queryset = queryset.filter(tags=tag)
        return queryset.distinct()