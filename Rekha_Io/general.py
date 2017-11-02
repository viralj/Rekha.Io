from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from plugins.request_params import get_request_param, REQUEST_LOGIN


def two_days_hence():
    """
    To return time after 48 hours.
    :return:
    """
    return timezone.now() + timezone.timedelta(days=2)


def two_days_ago():
    """
    To return time after 48 hours.
    :return:
    """
    return timezone.now() - timezone.timedelta(days=2)


def get_ri_login_with_param():
    return HttpResponseRedirect(reverse('accounts:action') + get_request_param(REQUEST_LOGIN))