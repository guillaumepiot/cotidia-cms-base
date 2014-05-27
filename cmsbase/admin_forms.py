import json
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from form_utils.forms import BetterModelForm

from .models import Page, PageTranslation

FIELD_CLASS_MAP = {
    'charfield': {
        'field_class':forms.CharField,
        'field_widget':forms.TextInput,
    },
    'textfield': {
        'field_class':forms.CharField,
        'field_widget':forms.Textarea,
    },
    'pagelinkfield': {
        'field_class':forms.ModelChoiceField,
        'field_widget':forms.Select,
        'field_choices':Page.objects.get_originals()
    }
}

class TranslationForm(BetterModelForm):
    required_css_class = 'required'
    error_css_class = 'errorfield'
    
    class Meta:
        model = PageTranslation
        exclude = ['content']

    def __init__(self, page, *args, **kwargs):

        super(TranslationForm, self).__init__(*args, **kwargs)

        self._fieldsets = [
            ('main', {'fields': ['parent', 'language_code', 'title', 'slug',], 'legend': 'Settings'}),
            # ('Advanced', {
            #     'fields': ['three', 'one'],
            #     'legend': 'The fieldset legend',
            #     'description': 'advanced stuff',
            #     'classes': ['advanced', 'collapse']
            #     }
            # )
        ]

        # Make parent field hidden
        self.fields['parent'] = forms.ModelChoiceField(queryset=Page.objects.get_originals(), widget=forms.HiddenInput())

        self.json_fields = page.mask.get_fields()

        # Go through each fieldset
        for fieldset in self.json_fields:
            fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
            _fields = []
            for field in fieldset['fields']:

                # Get the name of the field
                field_name = '%s_%s' % (fieldset_id, field['name'])
                field_label = field['name'].replace('_', ' ').capitalize()

                # Get the field class from the field map
                field_type = field['type']
                field_class = FIELD_CLASS_MAP[field_type]['field_class']
                field_widget = FIELD_CLASS_MAP[field_type]['field_widget']

                # Get the required option
                field_required = field['required']

                # Create a new form field
                
                if field_type in ['pagelinkfield']:
                    self.fields[field_name] = field_class(required=field_required, label=field_label, queryset=FIELD_CLASS_MAP[field_type]['field_choices'])
                else:
                    self.fields[field_name] = field_class(max_length=250, required=field_required, label=field_label, widget=field_widget)

                # Push the field name to the temporary field list
                _fields.append(field_name)

            fieldset = (fieldset['fieldset'],{'fields':_fields, 'legend':fieldset['fieldset']})
            self._fieldsets.append(fieldset)

        if self.instance:
            try:
                mask_data = json.loads(self.instance.content)
            except:
                mask_data = None
                
            if mask_data:

                # Go through each fieldset
                for fieldset in self.json_fields:
                    fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
                    for field in fieldset['fields']:

                        # Get the name of the field
                        field_name = '%s_%s' % (fieldset_id,field['name'])

                        # Set the initial value from the current data
                        self.fields[field_name].initial = mask_data.get(field_name, '')

    def save(self, *args, **kwargs):
        super(TranslationForm, self).save(*args, **kwargs)

        mask_data = {}

        # Create the mask data for each field
        for fieldset in self.json_fields:
            fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
            for field in fieldset['fields']:

                # Get the field type
                field_type = field['type']
                # Get the name of the field
                field_name = '%s_%s' % (fieldset_id,field['name'])

                if field_type in ['pagelinkfield']:
                    if self.cleaned_data[field_name]:
                        mask_data[field_name] = self.cleaned_data[field_name].id
                else:
                    mask_data[field_name] = self.cleaned_data[field_name]

        self.instance.content = json.dumps(mask_data)
        self.instance.save()

        return self.instance