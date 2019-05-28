from django.forms import  ModelForm
from django import forms
from .models import User, HostelOwner, Student

class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width:300px;'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width:300px;'}))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['user_type'].required = False

    class Meta:
        model= User
        fields = ['first_name','last_name','user_name','password','confirm_password','email','contact','user_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width:300px;'}),
            'last_name': forms.TextInput(attrs={'style': 'width:300px;'}),
            'user_name': forms.TextInput(attrs={'style': 'width:100%'}),
            'email': forms.TextInput(attrs={'style': 'width:300px;'}),
            'contact': forms.TextInput(attrs={'style': 'width:300px;'}),
            'user_type': forms.HiddenInput(),
        }

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        try:
            match = User.objects.get(user_name=user)
        except:
            return self.cleaned_data['user_name']
        raise forms.ValidationError('Username already exists...')

    def cleam_email(self):
        email = self.cleaned_data['email']
        try:
            mt = validate_email(email)
        except:
            return forms.ValidationError("Invalid Email......")
        return email

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        cpwd = self.cleaned_data['confirm_password']
        MIN_LENGTH = 8
        if pwd and cpwd :
            if pwd != cpwd:
                raise forms.ValidationError("password and confirm password doesn't match.")
            else:
                if len(pwd)<MIN_LENGTH:
                    raise forms.ValidationError("Password length must be greater than or equal to 8.")
                if  pwd.isdigit():
                    raise forms.ValidationError("password should not contain all numeric.")


class StudentForm(ModelForm):
    class Meta:
        model= Student
        fields = ['institute','gender','date_of_birth']
        widgets = {
            'institute': forms.TextInput(attrs={'style': 'width:300px;'}),
            'date_of_birth': forms.DateInput(format="%m/%d/%Y",attrs={'style': 'width:145px;'})
        }

class LogInForm(forms.Form):
    USER_TYPE_CHOICE = {
        ('X',"----Select---"),
        ('O', 'Hostel_Owner'),
        ('S', 'Student'),
    }
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:300px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width:300px;'}))
    user_type = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width:300px;'}),choices=USER_TYPE_CHOICE)
    class Meta:
        fields = ['username','password','user_type']
