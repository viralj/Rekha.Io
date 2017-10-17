# Create your views here.
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from accounts.forms import UserCreationForm, UserLoginForm
from accounts.models import UserAccountAction, User
from plugins.request_params import get_request_param, REQUEST_LOGIN


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
            'signup_form': UserCreationForm(),
            'login_form': UserLoginForm(),
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
            signup = UserCreationForm(request=request, data=request.POST)

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
            login = UserLoginForm(request=request, data=request.POST)

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

                return HttpResponseRedirect(reverse('accounts:action') + get_request_param(REQUEST_LOGIN))

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
        return HttpResponseRedirect(reverse('accounts:action'))


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

            return HttpResponseRedirect(reverse('accounts:action') + get_request_param(REQUEST_LOGIN))

        except UserAccountAction.DoesNotExist:
            messages.add_message(request, messages.ERROR, self.action_messages['broken_url'])

            return HttpResponseRedirect(reverse('accounts:action'))
