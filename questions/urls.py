"""
Url file for all accounts related urls
"""

from django.conf.urls import url

from questions.views import RIAskQuestion

urlpatterns = [
    # to display signup and login forms
    # url(r'^action/?$', RIAccountsAction.as_view(), name="action"),

    url(r'^ask?$', RIAskQuestion.as_view(), name="ask"),
]
