from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Address, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =(
            'username',
            'email',
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields =(
            "username",
            'email',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the 'password' field from the form
        self.fields.pop('password')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street_address', 'city', 'region', 'zip_code',)