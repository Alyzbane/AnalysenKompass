from django import forms
from django.forms import formset_factory

from polls.models import Choice

class ChoiceAddForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True })
        }