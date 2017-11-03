import json

from django import forms


class RIHelperModelForm(forms.ModelForm):
    """
    Helper model form so other model forms can extend and inherit following methods.
    """

    def __init__(self, *args, **kwargs):
        super(RIHelperModelForm, self).__init__(*args, **kwargs)

    def get_json_form(self):
        result = []
        for name, field in self.fields.items():
            result.append({'id': "id_{}".format(name), 'data': self.field_to_dict(field)})

        print(result)
        print(json.dumps(result))

        return ""

    def field_to_dict(self, field):
        x = {
            "type": str(field.__class__.__name__),
            "hidden": field.widget.is_hidden,
            "required": field.widget.is_required,
            "label": field.label,
            "help_text": field.help_text,
            "min_length": field.min_length,
            "max_length": field.max_length,
            "initial_value": field.initial,
            "widget": str(field.widget.__class__.__name__),
            "attrs": field.widget.attrs,
        }

        if 'data-field-type' in field.widget.attrs:
            x.update({"field_type": field.widget.attrs['data-field-type']})

        return x
