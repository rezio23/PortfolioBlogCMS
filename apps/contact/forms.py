from django import forms
from django.core.exceptions import ValidationError

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "name": "Your name",
            "email": "you@example.com",
            "subject": "What would you like to talk about?",
            "message": "Share your message, idea, or project details here.",
        }
        autocomplete = {
            "name": "name",
            "email": "email",
            "subject": "off",
            "message": "off",
        }
        field_error_messages = {
            "name": "Please enter your name.",
            "email": "Please enter your email address.",
            "subject": "Please enter a subject.",
            "message": "Please enter your message.",
        }
        field_attrs = {
            "name": {
                "pattern": "[^0-9]+",
                "title": "Name cannot contain numbers.",
            },
            "email": {
                "pattern": "[a-z0-9._%+\\-]+@[a-z0-9.\\-]+\\.[a-z]{2,}",
                "title": "Email must use lowercase letters only.",
            },
        }

        for name, field in self.fields.items():
            field.required = True
            field.error_messages["required"] = field_error_messages[name]
            field.widget.attrs.setdefault("placeholder", placeholders.get(name, ""))
            field.widget.attrs.setdefault("autocomplete", autocomplete.get(name, "off"))
            field.widget.attrs.setdefault("required", True)

            for attr_name, attr_value in field_attrs.get(name, {}).items():
                field.widget.attrs.setdefault(attr_name, attr_value)

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if any(character.isdigit() for character in name):
            raise ValidationError("Name cannot contain numbers.")
        return name

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        if email != email.lower():
            raise ValidationError("Email must use lowercase letters only.")
        return email
