from django import forms
from django.utils.translation import ugettext_lazy as _

class SubscribeForm(forms.Form):
	email = forms.EmailField(error_messages={'invalid': _('This email doesn\'t seem to be right!'), 'required':_('Please enter your email')})

class SearchForm(forms.Form):
	query = forms.CharField(error_messages={'required':_('Please enter your search query')}, widget=forms.TextInput(attrs={'placeholder':_('Search...')}))
	location = forms.CharField(required=False, widget=forms.HiddenInput())
	content_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
