"""
Url file for all accounts related urls
"""

from django.conf.urls import url

from questions.views import *

urlpatterns = [
    # to display signup and login forms
    # url(r'^action/?$', RIAccountsAction.as_view(), name="action"),

    # Ask question page
    url(r'^ask$', RIAskQuestion.as_view(), name="ask"),

    # Ask question post action page
    url(r'^ask/Action$', RIAskQuestionAction.as_view(), name="ask_action"),
]
