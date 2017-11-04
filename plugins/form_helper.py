import json

from django import forms

from Rekha_Io.settings import DEBUG


class RIHelperModelForm(forms.ModelForm):
    """
    Helper model form so other model forms can extend and inherit following methods.
    """

    x = {}

    def __init__(self, *args, **kwargs):
        super(RIHelperModelForm, self).__init__(*args, **kwargs)

    def get_json_form(self):
        result = []
        for name, field in self.fields.items():
            result.append({'id': "id_{}".format(name), 'data': self.field_to_dict(field)})

        return json.dumps(result)

    def field_to_dict(self, field):

        if not DEBUG:
            self.x = {
                "type": str(field.__class__.__name__),
                "widget": str(field.widget.__class__.__name__),
            }

        if hasattr(field, 'help_text'):
            self.x.update({"help_text": field.help_text})

        if hasattr(field, 'label'):
            self.x.update({"label": field.label})

        if hasattr(field, 'initial'):
            self.x.update({"initial_value": field.initial})

        if hasattr(field, 'min_length'):
            self.x.update({"min_length": field.min_length})

        if hasattr(field, 'max_length'):
            self.x.update({"max_length": field.max_length})

        if hasattr(field, 'widget.is_hidden'):
            self.x.update({"hidden": field.widget.is_hidden})

        if hasattr(field.widget, 'is_required'):
            self.x.update({"required": field.widget.is_required})

        if hasattr(field.widget, 'attrs'):
            self.x.update({"attrs": field.widget.attrs})

        if 'data-field-type' in field.widget.attrs:
            self.x.update({"field_type": field.widget.attrs['data-field-type']})

        return self.x
