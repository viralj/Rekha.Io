from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Plugins(models.Model):
    """
    This Plugins model will hold plugin details whether it is active or not.
    """
    plugin_hash = models.CharField(_('plugin unique hash'), max_length=250, null=False)
    is_active = models.BooleanField(_('is active?'), default=False, help_text=_('is plugin active?'))
