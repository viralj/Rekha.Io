import json

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

        title_parent = {"t": "p"}
        details_parent = {"d": "p"}
        tags_parent = {"d": "p"}

        widgets = {
            'title': forms.TextInput(attrs={
                'type': 'text',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'maxlength': 250,
                'data-parent': json.dumps(title_parent)
            }),
            'details': forms.TextInput(attrs={
                'type': 'textarea',
                'data-field-type': 'textarea',
                'data-parent': json.dumps(details_parent)
            }),
            'tags': forms.TextInput(attrs={
                'type': 'text',
                'data-field-type': 'text',
                'autocomplete': 'off',
                'data-parent': json.dumps(tags_parent)
            }),
        }

        labels = {
            "tags": _("Tags")
        }
