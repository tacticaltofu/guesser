from django import forms
from django.core.exceptions import ValidationError

class GuessPunchlineForm(forms.Form):
	punchline = forms.CharField(max_length=100)

	def clean_punchline(self):
		data = self.cleaned_data['punchline']
		return data