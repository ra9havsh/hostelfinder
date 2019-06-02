from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from .forms import RegistrationForm, StudentForm, LogInForm, SearchForm
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from hostelAdmin.forms import HostelForm, RoomForm, FeeForm, RoomDetailForm, ImageForm
from webpage.models import User, HostelOwner, Student, Rating
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

    if request.method=="GET":
        search_form = SearchForm(request.GET)
        district = request.GET.get('district')
        street = request.GET.get('street')
        hostel_type =request.GET.get('hostel_type')
        seater_type = request.GET.get('seater_type')
        quantity = request.GET.get('quantity')
        price_range1 =request.GET.get('price_range1')
        price_range2 = request.GET.get('price_range2')

        searched = False
        hostel = Hostel.objects.all()

        if district:
            hostel = hostel.filter(location__district__icontains=district)
            searched = True

        if street:
            hostel = hostel.filter(location__street__icontains=street)
            searched = True

        if hostel_type and hostel_type!='A':
            hostel = hostel.filter(hostel_type=hostel_type)
            searched = True

        if seater_type:
            hostel = hostel.filter(room__seater_type=seater_type)
            searched = True

        if quantity:
            hostel = hostel.filter(room__quantity=quantity)
            searched = True

        if price_range1:
            hostel = hostel.filter(fee__admission_fee__gte=price_range1)
            searched = True

        if price_range2:
            hostel = hostel.filter(fee__admission_fee__lte=price_range2)
            searched = True

        if searched:
            paginator = Paginator(hostel, 18)  # Show 18 contacts per page
            page = request.GET.get('page')
            hostels = paginator.get_page(page)
            return render(request,'webpage/search_result.html',{'hostels':hostels})
    else:
        search_form = SearchForm()

    args = {}
    args["search_form"] = search_form

    return render(request,'webpage/home_page.html',args)

def HostelDetailView(request, pk):
    hostel = Hostel.objects.get(id=pk)

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
        args = {'hostel':hostel,'username':user.user_name}
    else:
        args = {'hostel':hostel}
    return render(request,'webpage/hostel_detail.html',args)

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
        if request.method == "GET":
            search_form = SearchForm(request.GET)
            district = request.GET.get('district')
            street = request.GET.get('street')
            hostel_type = request.GET.get('hostel_type')
            seater_type = request.GET.get('seater_type')
            quantity = request.GET.get('quantity')
            price_range1 = request.GET.get('price_range1')
            price_range2 = request.GET.get('price_range2')

            searched = False
            hostel = Hostel.objects.all()

            if district:
                hostel = hostel.filter(location__district__icontains=district)
                searched = True

            if street:
                hostel = hostel.filter(location__street__icontains=street)
                searched = True

            if hostel_type and hostel_type != 'A':
                hostel = hostel.filter(hostel_type=hostel_type)
                searched = True

            if seater_type:
                hostel = hostel.filter(room__seater_type=seater_type)
                searched = True

            if quantity:
                hostel = hostel.filter(room__quantity=quantity)
                searched = True

            if price_range1:
                hostel = hostel.filter(fee__admission_fee__gte=price_range1)
                searched = True

            if price_range2:
                hostel = hostel.filter(fee__admission_fee__lte=price_range2)
                searched = True

            if searched:
                paginator = Paginator(hostel, 18)  # Show 18 contacts per page
                page = request.GET.get('page')
                hostels = paginator.get_page(page)
                return render(request, 'webpage/search_result.html', {'hostels': hostels,'username':user.user_name})
        else:
            search_form = SearchForm()

        args = {}
        args["search_form"] = search_form
        args["username"] = user.user_name
        args["user_id"] = user_id
        return render(request, 'webpage/home_page.html',args)
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

def rating(request,pk,rate):
    if 'user_id' in request.session:
        hostel = Hostel.objects.get(id=pk)
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        rating = Rating.objects.filter(user=user,hostel=hostel).exists()
        if not rating:
            rating = Rating.objects.create(user=user,hostel=hostel,rating=rate)
        else:
            rating = Rating.objects.filter(user=user,hostel=hostel).update(rating=rate)

    return redirect("webpage:hostel_details",pk)