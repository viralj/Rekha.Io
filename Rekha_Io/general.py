from django.utils import timezone


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