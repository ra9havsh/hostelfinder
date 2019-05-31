from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import RegistrationForm, StudentForm, LogInForm, SearchForm
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from hostelAdmin.forms import HostelForm, RoomForm, FeeForm, RoomDetailForm, ImageForm
from webpage.models import User, HostelOwner, Student
import json

def log_in_session(request):
    if 'user_id' in request.session:
        user = get_object_or_404(User,id = request.session['user_id'])

        if user.user_type=='O':
            return redirect("webpage:user_hostel_owner",user.id)
        else:
            return redirect("webpage:user_student",user.id)

def log_out(request):
    if request.session.has_key('user_id'):
        request.session.flush()
        return redirect("webpage:homepage")

def homepage(request):
    if 'user_id' in request.session:
        return log_in_session(request)

    if request.method=="POST":
        pass
    else:
        search_form = SearchForm()

    args = {}
    args["search_form"] = search_form

    return render(request,'webpage/home_page.html',args)

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
            if data['user_type']=='O':
                return redirect("webpage:user_hostel_owner",user.id)
            else:
                return redirect("webpage:user_student",user.id)

    else:
        form =  LogInForm(initial={'user_type':'X'})
    return render(request,'webpage/login_form.html', {'form':form} )

def user_hostel_owner(request,user_id):
    if 'user_id' in request.session and int(user_id)==request.session['user_id']:
        user_id =int(user_id)
        user = get_object_or_404(User,id = user_id)
        hostel_owner = HostelOwner.objects.filter(user=user).exists()

        if not hostel_owner:
            return formHostel(request,user.user_name)

        return render(request, 'webpage/user_page.html', {'username': user.user_name})
    else:
        raise Http404('Page not found with user Id : '+ user_id)

def user_student(request,user_id):
    if 'user_id' in request.session:
        user = get_object_or_404(User,id = request.session['user_id'])
        return render(request, 'webpage/user_page.html', {'username': user.user_name})
    else:
        raise Http404('Page not found with user Id : ' + user_id)

def formHostel(request,username):
    if request.method == "POST":
        hostel_form = HostelForm(request.POST)
        room_form = RoomForm(request.POST)
        fee_form = FeeForm(request.POST)
        image_form = ImageForm(request.POST,request.FILES)
        roomDetail_form = RoomDetailForm(request.POST)
        data = roomDetail_form.data['room_detail']

        if hostel_form.is_valid() and fee_form.is_valid() and image_form.is_valid():
            hostel = hostel_form.save()
            room = room_form.save(False)
            fee = fee_form.save(False)
            image = image_form.save(False)

            if data:
                data = json.loads(roomDetail_form.data['room_detail'])
                print(data)

                for x in data:
                   r = Room()
                   r.hostel=hostel
                   r.seater_type=x['seater_type']
                   r.quantity=x['quantity']
                   r.room_price=x['room_price']
                   r.save()

            room.hostel =hostel
            fee.hostel = hostel
            image.hostel = hostel
            fee.save()
            image.save()
            user = User.objects.get(id=request.session['user_id'])
            hostel_owner = HostelOwner()
            hostel_owner.user = user
            hostel_owner.hostel = hostel
            hostel_owner.save()
            return redirect("webpage:user_hostel_owner",request.session['user_id'])

    else:
        hostel_form = HostelForm()
        room_form = RoomForm()
        fee_form = FeeForm()
        roomDetail_form = RoomDetailForm()
        image_form = ImageForm()

    args = {}
    #args.update(csrf(request))
    args['hostel_form'] = hostel_form
    args['room_form'] = room_form
    args['fee_form'] = fee_form
    args['roomDetail_form'] = roomDetail_form
    args['image_form'] = image_form

    return render(request, 'webpage/hostel_registration.html',{'args':args,'username':username,'user_id':request.session['user_id']})