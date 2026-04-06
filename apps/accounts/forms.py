from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{classes} auth-login__input".strip()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_attrs = {
            "username": {
                "placeholder": "Choose a username",
                "autocomplete": "username",
            },
            "first_name": {
                "placeholder": "Enter your first name",
                "autocomplete": "given-name",
            },
            "last_name": {
                "placeholder": "Enter your last name",
                "autocomplete": "family-name",
            },
            "email": {
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            },
            "password1": {
                "placeholder": "Create a secure password",
                "autocomplete": "new-password",
            },
            "password2": {
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            },
        }

        self.fields["email"].label = "Email address"
        self.fields["email"].help_text = "We will use this for password recovery and account updates."

        for field_name, attrs in field_attrs.items():
            if field_name not in self.fields:
                continue

            field = self.fields[field_name]
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{classes} auth-login__input auth-register__input".strip()
            field.widget.attrs.update(attrs)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "location", "website", "profile_image")

