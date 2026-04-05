from django import forms

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

        for name, field in self.fields.items():
            field.widget.attrs.setdefault("placeholder", placeholders.get(name, ""))
            field.widget.attrs.setdefault("autocomplete", autocomplete.get(name, "off"))
