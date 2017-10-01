from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    CustomUserManager to create user and process other functions.
    """

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model:

    This model will handle `User` table in database and will store User related information.
    """

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(_('username'), max_length=10, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_(''))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        """
        To get absolute url for user's profile

        :return: user's profile url
        """
        return "/u/{}".format(urlquote(self.username))

    def get_full_name(self):
        """
        Returns the full name by first and last name, with a space in between.
        """
        return "{} {}".format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        """
        Returns short name, first name.
        :return: first_name
        """
        return self.first_name.strip()
