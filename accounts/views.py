# Create your views here.
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from Rekha_Io.general import get_ri_login_with_param
from accounts.forms import RIUserCreationForm, RIUserLoginForm, RIUserPasswordResetForm
from accounts.models import UserAccountAction, User
from plugins.backends import RIUserActivationEmailSender
from plugins.password_reset_helper import RIUserPasswordRecoveryEmailSender


class RIAccountsLoginRedirect(TemplateView):
    """
    To handle Django's default login redirect
    """
    def get(self, request, *args, **kwargs):
        next_redirect = request.GET.get("next", None)

        if next_redirect is not None:
            next_redirect = {"_next": next_redirect}

        return get_ri_login_with_param(next_redirect)

    def post(self, request, *args, **kwargs):
        next_redirect = request.GET.get("next", None)

        if next_redirect is not None:
            next_redirect = {"_next": next_redirect}

        return get_ri_login_with_param(next_redirect)


class RIAccountsAction(TemplateView):
    """
    This class will handle request for Accounts Action page where Sign up form and Login form will be displayed.
    """

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        context = {
            'signup_form': RIUserCreationForm(),
            'login_form': RIUserLoginForm(),
            'next_redirect': request.GET.get("_next", None),
        }

        return TemplateResponse(request, "accounts/action.html", context)


class RIAccountsActionSignup(TemplateView):
    """
    This class will handle signup request.
    """

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        if request.POST:
            signup = RIUserCreationForm(request=request, data=request.POST)

            if signup.is_valid():
                signup.save()
            else:
                for e in signup.non_field_errors():
                    messages.add_message(request, messages.ERROR, str(e))

        return HttpResponseRedirect(reverse('accounts:action'))


class RIAccountsActionLogin(TemplateView):
    """
    This class will handle login request.
    """

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(RIAccountsActionLogin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        if request.POST:
            login = RIUserLoginForm(request=request, data=request.POST)

            next_redirect = request.GET.get("_next", None)

            if login.is_valid():

                """
                If login form is valid, checking for next redirect url.

                If redirect url found, check if http, https or // exist in url. If found, redirect user to home page
                else check if redirect url starts with / or not and redirect user to that url based on existence of /
                in requested url.

                No need to worry about url path if it actually exist in system or not because Page Not Found will handle
                the error and 404 page will be displayed.
                """
                if next_redirect is not None:

                    if "http://" in str(next_redirect) or "https://" in str(next_redirect) or "//" in str(
                            next_redirect):
                        return HttpResponseRedirect("/")
                    elif str(next_redirect).startswith("/"):
                        return HttpResponseRedirect(next_redirect)
                    else:
                        return HttpResponseRedirect("/" + str(next_redirect))
                else:
                    return HttpResponseRedirect("/")
            else:
                for e in login.non_field_errors():
                    messages.add_message(request, messages.ERROR, str(e))

                return get_ri_login_with_param()

        return HttpResponseRedirect(reverse('accounts:action'))


class RIAccountsActionLogout(TemplateView):
    """
    To logout users.
    """

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        logout(request)
        return get_ri_login_with_param()


class RIAccountsActionActivate(TemplateView):
    """
    This class will handle account activation request.

    System will check for unused unique_code for specific user assigned. If record is found, system will
    activate user's account and it will be updated as verified email.
    """

    action_messages = {
        "email_verified": "Your email is verified and account is activated. You can login now.",
        "broken_url": "System ran into broken url. Please check your url."
    }

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        unique_code = kwargs.get('unique_code')
        username = kwargs.get('username')

        try:
            uaa = UserAccountAction.objects.get(is_used=False, unique_code=unique_code,
                                                belongs_to_user=User.objects.get(username=username),
                                                action_type=UserAccountAction.ACCOUNT_ACTIVATION)
            uaa.belongs_to_user.email_verified = True
            uaa.belongs_to_user.save()

            uaa.is_used = True
            uaa.save()

            messages.add_message(request, messages.SUCCESS, self.action_messages['email_verified'])

            return get_ri_login_with_param()

        except UserAccountAction.DoesNotExist:
            messages.add_message(request, messages.ERROR, self.action_messages['broken_url'])

            return HttpResponseRedirect(reverse('accounts:action'))


class RIAccountsActionRequest(TemplateView):
    """
    This class will handle forgot password request request.
    """

    user = None
    error_messages = {
        "email_not_found": "Entered email address not found in system.",
        "account_not_active": "Your account is not active! "
                              "Please check your inbox for more information or read community guideline.",
    }

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        if request.POST:
            try:
                self.user = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, self.error_messages['email_not_found'])

            if self.user is not None:
                if not self.user.is_active:
                    messages.add_message(request, messages.ERROR, self.error_messages['account_not_active'])
                else:
                    self.send_recovery_link_email()

        return HttpResponseRedirect(reverse('accounts:action'))

    def send_recovery_link_email(self):
        """
        This function will send email to user with recovery link in it.

        If user's email address is not verified, we will send activation link again to the email address otherwise
        password recovery link will be sent.

        :return:
        """

        if self.user.email_verified:
            # Password recovery helper
            RIUserPasswordRecoveryEmailSender(user=self.user, request=self.request)
        else:
            # Activation email plugin
            RIUserActivationEmailSender(user=self.user, request=self.request, resend_activation=True)


class RIAccountsActionPasswordReset(TemplateView):
    """
    This class will handle request for Password Reset Action page.
    """
    context = None

    error_messages = {
        'invalid_url': "Please check your reset password link or request new!",
        'password_updated': "Your password is successfully updated. You can now login with your new password!"
    }

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        user = uaa = None
        try:
            user = User.objects.get(username=kwargs.get('username'), is_active=True, email_verified=True)

            try:
                uaa = UserAccountAction.objects.get(belongs_to_user=user,
                                                    unique_code=kwargs.get('unique_code'),
                                                    is_used=False,
                                                    action_type=UserAccountAction.ACCOUNT_PASSWORD_RECOVERY,
                                                    expires__gte=timezone.now())

                self.context = {
                    'password_reset_form': RIUserPasswordResetForm(user=user)
                }
            except UserAccountAction.DoesNotExist:
                uaa = self.context = None

        except User.DoesNotExist:
            user = self.context = None

        if self.context is None:
            messages.add_message(request, messages.ERROR, self.error_messages['invalid_url'])
            return HttpResponseRedirect(reverse('accounts:action'))

        if request.method == "POST":
            f = RIUserPasswordResetForm(user=user, data=request.POST)

            if f.is_valid():
                f.save(commit=True)
                uaa.is_used = True
                uaa.save()

                messages.add_message(request, messages.SUCCESS, self.error_messages['password_updated'])
                return get_ri_login_with_param()
            else:
                for e in f.non_field_errors():
                    messages.add_message(request, messages.ERROR, str(e))

        return TemplateResponse(request, "accounts/password_reset.html", self.context)
