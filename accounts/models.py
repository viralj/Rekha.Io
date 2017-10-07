from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
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
    is_active = models.BooleanField(_('active'), default=False, help_text=_('is user active?'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USER_TYPES = (
        (0, 'developer'),
        (1, 'manager'),
        (2, 'educator'),
        (3, 'student'),
    )

    user_type = models.CharField(choices=USER_TYPES, default=3, max_length=2)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

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
        :return:
        """
        return self.first_name.strip()


class UserAccountAction(models.Model):
    """
    This model will hold user's account action data. This will be used for user's account verification and recovery.
    """
    ACCOUNT_ACTIVATION = 0
    ACCOUNT_PASSWORD_RECOVERY = 1

    unique_code = models.CharField(_('unique code'), max_length=254, null=False)
    belongs_to_user = models.ForeignKey('User', null=False, help_text=_('belongs to user'))
    action_type = models.IntegerField(_('action type'), null=False)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True, null=False)
    expires = models.DateTimeField(_('expires'), auto_now_add=False, null=False)
    last_modified = models.DateTimeField(_('last modified'), auto_now_add=True, null=False)
    is_used = models.BooleanField(_('is used'), default=False)
