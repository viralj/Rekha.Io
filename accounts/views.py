# Create your views here.
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.forms import UserCreationForm, UserLoginForm
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
        }

        return TemplateResponse(request, "accounts/action.html", context)


class RIAccountsActionSignup(TemplateView):
    """
    This class will handle signup request.
    """

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        if request.POST:
            signup = UserCreationForm(request.POST)

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

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        if request.POST:
            login = UserLoginForm(request=request, data=request.POST)

            if login.is_valid():
                return HttpResponseRedirect("/")
            else:
                for e in login.non_field_errors():
                    messages.add_message(request, messages.ERROR, str(e))

                return HttpResponseRedirect(reverse('accounts:action') + get_request_param(REQUEST_LOGIN))

        return HttpResponseRedirect(reverse('accounts:action'))
