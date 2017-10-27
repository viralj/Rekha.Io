"""
This middleware file will contain most plugin related middleware and related middleware.
"""

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from plugins.request_params import get_request_param, REQUEST_LOGIN

__author__ = "Viral Joshi"


class LoggedInRedirectMiddleware(MiddlewareMixin):
    """
    To redirect logged in users from specific urls.

    For eg: Redirect from Login page, Sign up page

    """
    path = ""

    def process_request(self, request):
        # Current path
        self.path = request.path_info.lstrip('/')

        # List of urls to redirect logged in users from
        redirect_urls_after_login = [
            reverse('accounts:action').lstrip('/'),
            reverse('accounts:action_login').lstrip('/'),
            reverse('accounts:action_signup').lstrip('/')
        ]

        restricted_urls = [
            # reverse('accounts:action_signup').lstrip('/')
        ]

        # Redirect user from specific pages and restrict access if user is logged in
        if self.path in redirect_urls_after_login and request.user.is_authenticated:
            return HttpResponseRedirect("/")

        # Redirect user from specific pages and restrict access if user is not logged in and prompt to login
        if self.path in restricted_urls and not request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('accounts:action') + get_request_param(REQUEST_LOGIN, {'_next': self.path}))

        return None
