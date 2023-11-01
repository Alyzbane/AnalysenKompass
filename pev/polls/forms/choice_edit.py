# forms.py
from django import forms

from polls.models import Choice
class ChoiceEditForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }
