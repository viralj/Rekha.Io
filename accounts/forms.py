import random
import re

from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from plugins.backends import RIUserActivationEmailSender


class UserCreationForm(forms.ModelForm):
    """
    Custom user creation form. This model form will be used for user signup
    """

    error_messages = {
        'email_registered': _('Email address is already registered with us!'),
        'username_taken': _('Username is taken! Please choose another username.'),
        'username_short': _('Username is too short, 5-15 characters only.'),
        'username_long': _('Username is too long, 5-15 characters only.'),
        'username_invalid': _('Username is not allowed. Alphanumeric, "-", "." and "-" allowed. '),
        'password_weak': _(
            "Password is short. Please select strong password, something like {}".format(
                "".join(random.sample("abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?", 12))
            )),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UserCreationForm, self).__init__(*args, **kwargs)

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

    def clean(self):
        """
        1) Checking if email is already registered or not. If email is already registered, we will throw an error
        2) Checking if username is taken or not. If username is taken, we will throw an error
        3) Checking username pattern
        4) Checking password length and throw error accordingly

        :return: cleaned_data
        """
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        username_pattern = "^[a-zA-Z0-9_.-]+$"

        # Step 1:
        try:
            u = User.objects.get(email=email)
            raise forms.ValidationError(self.error_messages['email_registered'], code='email_registered')
        except User.DoesNotExist:
            pass

        # Step 2:
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(self.error_messages['username_taken'], code='username_taken')
        except User.DoesNotExist:
            pass

        # Step 3
        if not re.match(username_pattern, username):
            raise forms.ValidationError(self.error_messages['username_invalid'], code='username_invalid')

        # Step 4:
        if len(password) < 10:
            raise forms.ValidationError(self.error_messages['password_weak'], code='password_weak')

        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        # Activation email plugin
        RIUserActivationEmailSender(user=user, request=self.request)

        return user


class UserLoginForm(AuthenticationForm):
    """
    User login form
    """

    username = UsernameField(
        max_length=255,
        min_length=6,
        widget=forms.TextInput(attrs={'autofocus': False, 'autocomplete': 'off'}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        min_length=10,
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = self.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user: User):
        if not user.is_active:
            raise forms.ValidationError("Your account is not activated yet! Please confirm your email.",
                                        code='inactive_user')
        else:
            login(request=self.request, user=user)

    def authenticate(self, username, password):
        """
        Custom authenticate method to authenticate user.

        Django's default authenticate method didn't work some how. I wrote this to authenticate and hopefully
        someday I or another contributor will be able to solve the issue with default authenticate method
        but until then, this method will be used.

        :param username:
        :param password:
        :return:    User or None
        """
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))

            if user.check_password(password):
                return user
            else:
                return None

        except User.DoesNotExist:
            return None
