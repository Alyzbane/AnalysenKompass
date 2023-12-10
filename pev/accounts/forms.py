from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=35, min_length=5,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # Profile fields
    sex = forms.ChoiceField(choices=Profile.SEX_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'sex']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'is_active']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#            'sex': forms.RadioSelect(choices=Profile.SEX_CHOICES),
        }