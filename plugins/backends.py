"""
This file contains all plugins for the project.
"""
import hashlib
import time

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from Rekha_Io.general import two_days_hence
from Rekha_Io.settings import RI_SITE_URL, EMAIL_HOST_USER
from accounts.models import User, UserAccountAction
from plugins.models import Plugins


class RIUserActivationEmailSender(object):
    """
    This class will handle user activation email process. This process/plugin will be used to verify new user's email
    id and activate Rekha.Io account.

    This plugin can be disabled and when it's disabled, it will just activate user's account.
    """
    plugin_hash = hashlib.sha256("RIUserActivationEmailSender".encode('utf-8')).hexdigest()

    action_messages = {
        "email_verified": "Please check your email for further action!",
        "account_created": "Your account is successfully created. You can login now to enjoy programmer's community."
    }

    def __init__(self, user: User, request):
        self.user = user
        self.request = request
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
            'user_username': self.user.username,
            'user_activation_link': self.activation_url_builder()
        }

        email_title = "Activate your Rekha.Io account!"
        email_html = render_to_string('plugins/user_activation_email.html', c)

        try:
            email = EmailMultiAlternatives(subject=email_title, body=strip_tags(email_html),
                                           from_email=EMAIL_HOST_USER, to=[self.user.email])
            email.attach_alternative(email_html, "text/html")
            email.send()

            messages.add_message(self.request, messages.SUCCESS, self.action_messages['email_verified'])

        except Exception as e:
            print("=====", str(e))

    def inactive_plugin(self):
        """
        Process when this plugin is inactive
        :return:
        """
        self.user.email_verified = True
        self.user.save()

        messages.add_message(self.request, messages.SUCCESS, self.action_messages['account_created'])

        return HttpResponseRedirect("/")

    def generate_activation_token(self):
        """
        Generating hash using user's id, email, user name and adding timestamp in it.

        Reason of adding time stamp is that we will be using same model for Account activation and Forget password
        so one user will have same hash everytime and to avoid that, just adding timestamp.

        :return: UserAccountAction unique_code
        """
        e_hash = hashlib.sha256(
            (str(self.user.id) + str(self.user.email) + str(self.user.username) + str(time.time())
             ).encode('utf-8')).hexdigest()

        uaa = UserAccountAction.objects.create(unique_code=e_hash, belongs_to_user=self.user,
                                               action_type=UserAccountAction.ACCOUNT_ACTIVATION,
                                               expires=two_days_hence())

        return uaa.unique_code

    def activation_url_builder(self):
        """
        Activation link builder for user which will return activation link.
        :return:
        """

        return RI_SITE_URL + reverse("accounts:action_activate", kwargs={
            'username': self.user.username,
            'unique_code': self.generate_activation_token()
        })
