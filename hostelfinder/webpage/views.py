from django.shortcuts import render
from .forms import RegistrationForm, StudentForm
#from hostelAdmin.models import Hostel, Location, Room, Fee, Image

def homepage(request):
    return render(request,'webpage/home_page.html')

def register_view(request):
    return render(request,'webpage/register.html')
2
def register_form_view(request,user_type):
    form = {}
    form['registration_form'] = RegistrationForm()
    form['student_form'] = StudentForm()
    args = {'user_type' : user_type, 'form':form }
    return render(request,'webpage/register_form.html',args)