"""
Url file for all accounts related urls
"""

from django.conf.urls import url

from accounts.views import *

urlpatterns = [
    # to display signup and login forms
    url(r'^action$', RIAccountsAction.as_view(), name="action"),

    # to process signup request
    url(r'^action/SignUp$', RIAccountsActionSignup.as_view(), name="action_signup"),

    # to process login request
    url(r'^action/Login$', RIAccountsAction.as_view(), name="action_login"),
]
