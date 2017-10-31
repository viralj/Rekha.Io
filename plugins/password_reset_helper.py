import hashlib
import time

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils import timezone

from Rekha_Io.general import two_days_hence, two_days_ago
from Rekha_Io.settings import RI_SITE_URL, EMAIL_HOST_USER
from accounts.models import User, UserAccountAction


class RIUserPasswordRecoveryEmailSender(object):
    """
    This class will handle user forgot password process.

    """

    action_messages = {
        'recovery_email_sent': "Password reset email sent. Please check your inbox for further steps."
    }

    def __init__(self, user: User, request):
        self.user = user
        self.request = request
        self.process()

    def process(self):
        """
        Process when this plugin is active
        :return:
        """

        c = {
            'user_full_name': self.user.get_full_name(),
            'user_username': self.user.username,
            'user_activation_link': self.recovery_url_builder()
        }

        email_title = "Activate your Rekha.Io account!"
        email_html = render_to_string('plugins/user_activation_email.html', c)

        try:
            email = EmailMultiAlternatives(subject=email_title, body=strip_tags(email_html),
                                           from_email=EMAIL_HOST_USER, to=[self.user.email])
            email.attach_alternative(email_html, "text/html")
            email.send()

            messages.add_message(self.request, messages.SUCCESS, self.action_messages['recovery_email_sent'])

        except Exception as e:
            print("=====", str(e))

    def generate_password_recovery_token(self):
        """
        Generating hash using user's id, email, user name and adding timestamp in it.

        Reason of adding time stamp is that we will be using same model for Account activation and Forget password
        so one user will have same hash everytime and to avoid that, just adding timestamp.

        # Adding random string into unique code hash because user id may be a key to keep it random and safe
        from being figured out, but just in case, one extra string won't hurt.

        :return: UserAccountAction unique_code
        """

        try:

            uaa = UserAccountAction.objects.get(belongs_to_user=self.user,
                                                action_type=UserAccountAction.ACCOUNT_PASSWORD_RECOVERY,
                                                is_used=False,
                                                expires__gte=timezone.now())
        except UserAccountAction.DoesNotExist:
            e_hash = hashlib.sha256(
                (str(self.user.id) + str(self.user.email) + str(self.user.username) + str(
                    time.time()) + get_random_string()
                 ).encode('utf-8')).hexdigest()

            uaa = UserAccountAction.objects.create(unique_code=e_hash, belongs_to_user=self.user,
                                                   action_type=UserAccountAction.ACCOUNT_PASSWORD_RECOVERY,
                                                   expires=two_days_hence())

        return uaa.unique_code

    def recovery_url_builder(self):
        """
        Recovery link builder for user which will return password reset link.
        :return:
        """

        return RI_SITE_URL + reverse("accounts:action_reset", kwargs={
            'username': self.user.username,
            'unique_code': self.generate_password_recovery_token()
        })
