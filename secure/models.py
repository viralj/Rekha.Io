from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class UsedPasswords(models.Model):
    """
    To store all user's used password for future reference and account security
    """

    belongs_to_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    password = models.CharField(_('used password'), null=False, max_length=255)
    date_created = models.DateTimeField(_('date record created'), default=timezone.now)
