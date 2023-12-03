from django import forms

from .models import Survey


class SurveyAddForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                          'rows': 5,
                                          'cols': 20}),
        }
