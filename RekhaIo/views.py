# Create your views here.
from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class RIHomePage(TemplateView):
    context = {}

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        return TemplateResponse(request, "home.html", self.context)
