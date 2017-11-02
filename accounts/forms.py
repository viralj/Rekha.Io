import random
import re

from django import forms
from django.contrib.auth import login, password_validation
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from plugins.backends import RIUserActivationEmailSender
from secure.models import UsedPasswords


class RIUserCreationForm(forms.ModelForm):
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
        super(RIUserCreationForm, self).__init__(*args, **kwargs)

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
        user = super(RIUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        # Activation email plugin
        RIUserActivationEmailSender(user=user, request=self.request)

        # Creating user password record
        UsedPasswords.objects.create(belongs_to_user=user, password=user.password)

        return user


class RIUserLoginForm(AuthenticationForm):
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


class RIUserPasswordResetForm(forms.Form):
    """
    This form will handle password reset request
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_used': _("Please use new password that you have not previously used."),
        'password_weak': _(
            "Password is short. Please select strong password, something like {}".format(
                "".join(random.sample("abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?", 12))
            )),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RIUserPasswordResetForm, self).__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )

        password_validation.validate_password(password2, self.user)

        """
        Checking if password was used previously
        """
        used_pass = UsedPasswords.objects.filter(belongs_to_user=self.user)

        if len(used_pass) > 0:
            for x in used_pass:
                if check_password(password, x.password):
                    raise forms.ValidationError(
                        self.error_messages['password_used'],
                        code='password_used',
                    )
        if len(password) < 10:
            raise forms.ValidationError(self.error_messages['password_weak'], code='password_weak')

        return cleaned_data

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
            # Creating user password record
            UsedPasswords.objects.create(belongs_to_user=self.user, password=self.user.password)
        return self.user
