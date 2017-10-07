"""
This file contains all plugins for the project.
"""
import hashlib

from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

from accounts.models import User
from plugins.models import Plugins


class RIUserActivationEmailSender(object):
    """
    This class will handle user activation email process. This process/plugin will be used to verify new user's email
    id and activate Rekha.Io account.

    This plugin can be disabled and when it's disabled, it will just activate user's account.
    """
    plugin_hash = hashlib.sha256("RIUserActivationEmailSender".encode('utf-8')).hexdigest()

    def __init__(self, user: User):
        self.user = user

        try:
            plugin, created = Plugins.objects.get_or_create(plugin_hash=self.plugin_hash)

            if plugin.is_active:
                self.active_plugin()
            else:
                self.inactive_plugin()

        except Exception:
            pass

    def active_plugin(self):
        """
        Process when this plugin is active
        :return:
        """

        c = {
            'user_full_name': self.user.get_full_name(),
            'user_username': self.user.username
        }

        msg_html = render_to_string('plugins/user_activation_email.html', c)

    def inactive_plugin(self):
        """
        Process when this plugin is inactive
        :return:
        """
        self.user.is_active = True
        self.user.save()

        return HttpResponseRedirect("/")

    
