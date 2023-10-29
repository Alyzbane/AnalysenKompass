from django import forms

from polls.models import Poll

class PollEditForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ['poll_text', ]
        widgets = {
            'poll_text': forms.Textarea(attrs={'class': 'form-control',
                                          'rows': 5,
                                          'cols': 20}),
        }