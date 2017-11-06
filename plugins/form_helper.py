import json

from django import forms

from Rekha_Io.settings import DEBUG


class RIHelperModelForm(forms.ModelForm):
    """
    Helper model form so other model forms can extend and inherit following methods.
    """

    def __init__(self, *args, **kwargs):
        super(RIHelperModelForm, self).__init__(*args, **kwargs)

    def get_form_as_list(self):
        """
        To create form as list object and return
        :return: form as list
        """
        result = []
        for name, field in self.fields.items():
            result.append({'id': "id_{}".format(name), 'data': self.field_to_dict(field)})
        return result

    def get_form_as_json(self):
        """
        To create form as json object and return
        :return: form as json
        """
        return json.dumps(self.get_form_as_list())

    def field_to_dict(self, field):
        """
        Creating dictionary object of field and returning dictonary
        :param field:
        :return: dictionary of form
        """
        input_field = {}
        x = {}
        if not DEBUG:
            x = {
                "type": str(field.__class__.__name__),
                "widget": str(field.widget.__class__.__name__),
            }

        # help text for input
        if hasattr(field, 'help_text'):
            x.update({"help_text": field.help_text})

        # label for input
        if hasattr(field, 'label'):
            x.update({"label": field.label})

        # place holder object for for input
        if hasattr(field, 'initial'):
            input_field.update({"placeholder": field.initial})

        # min length object for for input
        if hasattr(field, 'min_length'):
            input_field.update({"min_length": field.min_length})

        # max object for for input
        if hasattr(field, 'max_length'):
            input_field.update({"max_length": field.max_length})

        # hidden object for for input
        if hasattr(field, 'widget.is_hidden'):
            input_field.update({"hidden": field.widget.is_hidden})

        # is required object for for input
        if hasattr(field.widget, 'is_required'):
            input_field.update({"required": field.widget.is_required})

        # all attributes for for input
        if hasattr(field.widget, 'attrs'):
            x.update({"attrs": field.widget.attrs})

        # type object for for input
        if hasattr(field.widget.attrs, 'data-field-type'):
            input_field.update({"type": field.widget.attrs['data-field-type']})

        x.update({"input": input_field})
        return x
