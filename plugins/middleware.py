"""
This middleware file will contain most plugin related middleware and related middleware.
"""
from re import compile

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

__author__ = "Viral Joshi"


class LoggedInRedirectMiddleware(MiddlewareMixin):
    """
    To redirect logged in users from specific urls.

    For eg: Redirect from Login page, Sign up page

    """

    def process_request(self, request):
        # Current path
        path = request.path_info.lstrip('/')

        # List of urls to redirect logged in users from
        redirect_urls = [
            reverse('accounts:action').lstrip('/'),
            reverse('accounts:action_login').lstrip('/'),
            reverse('accounts:action_signup').lstrip('/')
        ]

        if path in redirect_urls and request.user.is_authenticated:
            return HttpResponseRedirect("/")

        return None
