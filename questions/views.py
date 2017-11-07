# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from questions.forms import RIAskQuestionForm


class RIAskQuestion(TemplateView):
    """
    This class will handle ask question view page
    """
    context = {}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.process(request, *args, **kwargs)

    def process(self, request, *args, **kwargs):
        self.context = {
            'ri_ask_q': json.dumps({
                'form': RIAskQuestionForm().get_form_as_list(),
                'post': reverse('questions:ask_action'),
            }),
        }
        return TemplateResponse(request, "questions/ask_question.html", self.context)


class RIAskQuestionAction(TemplateView):
    """
    This class will handle ask question post request to post a new question.
    """
    context = {}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        raise Http404
