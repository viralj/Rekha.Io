"""
Url file for all accounts related urls
"""

from django.conf.urls import url

from accounts.views import *

urlpatterns = [

    # to display signup and login forms
    url(r'^login/?$', RIAccountsLoginRedirect.as_view(), name="login_redirect"),

    # to display signup and login forms
    url(r'^action/?$', RIAccountsAction.as_view(), name="action"),

    # to process signup request
    url(r'^action/SignUp$', RIAccountsActionSignup.as_view(), name="action_signup"),

    # to process login request
    url(r'^action/Login$', RIAccountsActionLogin.as_view(), name="action_login"),

    # to process logout request
    url(r'^action/Logout$', RIAccountsActionLogout.as_view(), name="action_logout"),

    # to process account activation
    url(r'^action/activate/(?P<username>[\w.]{5,15})/(?P<unique_code>[\w]{0,255})$', RIAccountsActionActivate.as_view(),
        name="action_activate"),

    # to process activation email or account recovery
    url(r'^action/Request$', RIAccountsActionRequest.as_view(), name="action_request"),

    # to process password reset
    url(r'^action/reset/(?P<username>[\w.]{5,15})/(?P<unique_code>[\w]{0,255})$', RIAccountsActionPasswordReset.as_view(),
        name="action_reset"),

]
