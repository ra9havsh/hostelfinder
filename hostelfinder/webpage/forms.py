from django.forms import  ModelForm
from django import forms
from .models import User, HostelOwner, Student

class RegistrationForm(ModelForm):
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

class StudentForm(ModelForm):
    class Meta:
        model= Student
        fields = ['institute','gender','date_of_birth']
        widgets = {
            'institute': forms.TextInput(attrs={'style': 'width:300px;'}),
            'date_of_birth': forms.DateInput(format="%m/%d/%Y",attrs={'style': 'width:145px;'})
        }