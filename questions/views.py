# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from questions.forms import RIAskQuestionForm


class RIAskQuestion(TemplateView):
    """
    This class will
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
            'ask_form': RIAskQuestionForm().get_json_form()
        }
        return TemplateResponse(request, "questions/ask_question.html", self.context)
