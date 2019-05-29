from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistrationForm, StudentForm, LogInForm
#from hostelAdmin.models import Hostel, Location, Room, Fee, Image
from webpage.models import User
from django import forms

def log_in_session(request):
    if 'user_id' in request.session:
        user = get_object_or_404(User,id = request.session['user_id'])
        return render(request, 'webpage/user_page.html',{'end_user':user})

def log_out(request):
    if request.session.has_key('user_id'):
        request.session.flush()
        return redirect("webpage:homepage")

def homepage(request):
    if 'user_id' in request.session:
        return log_in_session(request)

    return render(request,'webpage/home_page.html')

def register_view(request):
    if 'user_id' in request.session:
        return log_in_session(request)

    return render(request,'webpage/register.html')

def register_form_view(request,user_type):
    if 'user_id' in request.session:
        return log_in_session(request)

    form = {}
    if request.method == "POST":
        if(user_type=="Hostel_Owner"):
            register_form = RegistrationForm(request.POST)
            student_form = StudentForm()

            if register_form.is_valid():
                user = register_form.save()
                return redirect("webpage:login")

        else:
            register_form = RegistrationForm(request.POST)
            student_form = StudentForm(request.POST)
            if register_form.is_valid() and student_form.is_valid():
                user = register_form.save()
                student = student_form.save(False)
                student.user = user
                student.save()
                return redirect("webpage:login")
    else:
        if(user_type=="Hostel_Owner"):
            register_form = RegistrationForm(initial={'user_type': 'O'})
        else:
            register_form = RegistrationForm(initial={'user_type': 'S'})
        student_form = StudentForm()

    form['registration_form'] = register_form
    form['student_form'] = student_form
    args = {'user_type' : user_type, 'form':form }
    return render(request,'webpage/register_form.html',args)

def login_form_view(request):
    if 'user_id' in request.session:
        return log_in_session(request)
        
    if request.method == "POST":
        form = LogInForm(request.POST)
        data = request.POST.copy()
        if form.is_valid():
            user = get_object_or_404(User,user_name=data['username'],password = data['password'],user_type=data['user_type'])
            request.session['user_id']=user.id
            return render(request,'webpage/user_page.html',{'end_user': user})

    else:
        form =  LogInForm(initial={'user_type':'X'})
    return render(request,'webpage/login_form.html', {'form':form} )