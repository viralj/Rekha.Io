from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    """
    Custom user creation form. This model form will be used for user signup
    """

    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]
        widgets = {
            'email': forms.TextInput(attrs={
                'type': 'email',
                'autocomplete': 'off'
            }),
            'password': forms.TextInput(attrs={
                'type': 'password',
                'minlength': '10'
            }),
            'username': forms.TextInput(attrs={
                'type': 'text',
                'minlength': '6',
                'autocomplete': 'off'
            }),
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'autocomplete': 'off'
            }),
            'last_name': forms.TextInput(attrs={
                'type': 'text',
                'autocomplete': 'off'
            })

        }

        labels = {
            'email': _('Enter email'),
            'username': _('Enter username'),
            'password': _('Enter password'),
            'first_name': _('Enter first name'),
            'last_name': _('Enter last name'),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    """
    User login form
    """

    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            'password': forms.TextInput(attrs={
                'type': 'password',
                'minlength': '10'
            }),
            'username': forms.TextInput(attrs={
                'type': 'text',
                'minlength': '6'
            })
        }

        labels = {
            'username': _('Username'),
            'password': _('Password'),
        }
