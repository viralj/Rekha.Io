"""
This middleware file will contain most plugin related middleware and related middleware.
"""

__author__ = "Viral Joshi"


class LoggedInRedirectMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
