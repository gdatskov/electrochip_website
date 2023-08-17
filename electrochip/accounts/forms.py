import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

    # TODO: add some validation
    def clean_username(self):
        username = self.cleaned_data.get("username")
        # if any(char.isdigit() for char in username):
        #     raise forms.ValidationError("Username cannot contain digits.")
        return username


def no_digits_validator(value):
    if re.search(r'\d', value):
        raise ValidationError('The field cannot contain digits.')


class EditUserProfileForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'profile_picture')
        # exclude = ('password',)
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'email': 'E-mail:',
            'profile_picture': 'Image:',
        }
    # TODO? What is this? Is needed?
    # first_name = forms.CharField(validators=[no_digits_validator], required=False)
    # last_name = forms.CharField(validators=[no_digits_validator], required=False)
