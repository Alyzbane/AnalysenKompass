# forms.py
from django import forms

from polls.models import Choice
class ChoiceEditForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', ]
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, })
        }
