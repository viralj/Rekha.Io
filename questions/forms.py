from django import forms
from django.utils.translation import ugettext as _

from plugins.form_helper import RIHelperModelForm
from questions.models import Question


class RIAskQuestionForm(RIHelperModelForm):
    """
    Ask question form using Question model
    """
    error_messages = {
        'email_registered': _('Email address is already registered with us!'),
    }

    def __init__(self, *args, **kwargs):
        super(RIAskQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ["title", "details", "tags"]

        title_parent = {"class": "col s12 m12 l12"}
        details_parent = {"class": "col s12 m12 l12"}
        tags_parent = {"class": "col s12 m12 l12"}

        widgets = {
            'title': forms.TextInput(attrs={
                'type': 'text',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'maxlength': 250,
                'data-parent': title_parent
            }),
            'details': forms.TextInput(attrs={
                'type': 'textarea',
                'data-field-type': 'textarea',
                'data-parent': details_parent
            }),
            'tags': forms.TextInput(attrs={
                'type': 'text',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'data-parent': tags_parent
            }),
        }

        labels = {
            "tags": _("Tags")
        }
