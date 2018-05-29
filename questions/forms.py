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

        title_parent = {"class": "input-field col s12 m12 l12", "id": "title"}
        details_parent = {"class": "input-field col s12 m12 l12", "id": "details"}
        tags_parent = {"class": "chips chips-placeholder input-field col s12 m12 l12", "id": "tags"}
        widgets = {
            'title': forms.TextInput(attrs={
                'type': 'text',
                'class': 'validate',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'maxlength': 250,
                'data_parent': title_parent
            }),
            'details': forms.Textarea(attrs={
                'type': 'textarea',
                'class': 'materialize-textarea',
                'data-field-type': 'textarea',
                'data_parent': details_parent
            }),
            'tags': forms.TextInput(attrs={
                'class': 'input',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'data_parent': tags_parent,
                'extra': {'chip': True, 'close': "<i class='close material-icons'>close</i>"}
            }),
        }

        labels = {
            "tags": _("Tags")
        }
