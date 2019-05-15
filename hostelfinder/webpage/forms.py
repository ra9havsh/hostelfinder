from django.forms import  ModelForm
from django import forms
from .models import User, HostelOwner, Student

class HostelOwnerRegistration(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width:300px;'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width:300px;'}))
    class Meta:
        model= User
        fields = ['first_name','last_name','user_name','password','confirm_password','email','contact']
        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width:300px;'}),
            'last_name': forms.TextInput(attrs={'style': 'width:300px;'}),
            'user_name': forms.TextInput(attrs={'style': 'width:100%'}),
            'email': forms.TextInput(attrs={'style': 'width:300px;'}),
            'contact': forms.TextInput(attrs={'style': 'width:300px;'}),
        }