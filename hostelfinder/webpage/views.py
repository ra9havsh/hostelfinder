from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from .forms import RegistrationForm, StudentForm, LogInForm, SearchForm
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from hostelAdmin.forms import HostelForm, RoomForm, FeeForm, RoomDetailForm, ImageForm
from webpage.models import User, HostelOwner, Student, Rating
import json

def popular_hostel():
    rating = Rating.objects.values_list('hostel','avg').order_by('-avg').distinct()[:9]
    hostel =[]
    for rating in rating:
        hostel.append(int(rating[0]))

    avg_hostel = Hostel.objects.filter(id__in=hostel)
    print(avg_hostel)
    return avg_hostel

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
    args['avg_hostels'] = popular_hostel()
    return render(request,'webpage/home_page.html',args)

def HostelDetailView(request, pk):
    hostel = get_object_or_404(Hostel,id=pk)
    # rating_hostel = Rating.objects.filter(hostel_id=pk).exists()
    #
    # if rating_hostel:
    #     total_rating = 0
    #     rating_hostel=Rating.objects.filter(hostel_id=pk)
    #     for rating in rating_hostel:
    #         total_rating = total_rating + rating.rating
    #     avg_rating = total_rating/len(rating_hostel)
    #
    #     if avg_rating<0.5:
    #         avg_rating=0
    #     elif avg_rating<1.5:
    #         avg_rating=1
    #     elif avg_rating<2.5:
    #         avg_rating=2
    #     elif avg_rating<3.5:
    #         avg_rating=3
    #     elif avg_rating<4.5:
    #         avg_rating=4
    #     else:
    #         avg_rating=5
    # else:
    #     avg_rating = 0

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.user_type=='O':
            hostel_owner = get_object_or_404(HostelOwner,user_id=user_id,hostel_id=pk)

        rating_user = Rating.objects.filter(user_id=user_id,hostel_id=pk).exists()

        if rating_user:
            rating_user = get_object_or_404(Rating,user_id=user_id, hostel_id=pk)
            args = {'hostel': hostel, 'username': user.user_name,'rating_user':rating_user.rating}
        else:
            args = {'hostel':hostel,'username':user.user_name}
    else:
        args = {'hostel':hostel}

    # args['avg_rating'] = avg_rating
    return render(request,'webpage/hostel_detail.html',args)

def HostelEditView(request, pk):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        hostel_owner = get_object_or_404(HostelOwner,user_id=user_id,hostel_id=pk)
        if request.method == "POST":
            hostel_form = HostelForm(request.POST,instance=Hostel.objects.get(id=pk))
            room_form = RoomForm(request.POST)
            fee_form = FeeForm(request.POST,instance=Fee.objects.get(hostel_id=pk))
            roomDetail_form = RoomDetailForm(request.POST)
            image_form = ImageForm(request.POST,request.FILES,instance=Image.objects.get(hostel_id=pk))
            data = roomDetail_form.data['room_detail']

            if hostel_form.is_valid() and fee_form.is_valid() and image_form.is_valid():
                hostel = hostel_form.save()
                room = room_form.save(False)
                fee = fee_form.save(False)
                image = image_form.save(False)

                Room.objects.filter(hostel_id=pk).delete()

                if data:
                    data = json.loads(roomDetail_form.data['room_detail'])

                    for x in data:
                        r = Room()
                        r.hostel = hostel
                        r.seater_type = x['seater_type']
                        r.quantity = x['quantity']
                        r.room_price = x['room_price']
                        r.available = x['available']
                        r.save()

                room.hostel =hostel
                fee.hostel = hostel
                image.hostel = hostel
                fee.save()
                image.save()

                return redirect("webpage:hostel_details",pk=pk)

        else:
            hostel_form = HostelForm(instance=Hostel.objects.get(id=pk))
            room_form = RoomForm()

            #for fill the list in the room_detail field in RoomDetailForm
            room = list(Room.objects.filter(hostel_id=pk))
            room_detail = []

            for x in room:
                room_detail.append({
                    'seater_type':x.seater_type,
                    'quantity':x.seater_type,
                    'room_price':x.room_price,
                    'available':x.available
                })

            roomDetail_form = RoomDetailForm(initial={'room_detail': json.dumps(room_detail)})
            fee_form = FeeForm(instance=Fee.objects.get(hostel_id=pk))
            image_form = ImageForm(instance=Image.objects.get(hostel_id=pk))

        args = {}
        #args.update(csrf(request))
        args['hostel_form'] = hostel_form
        args['room_form'] = room_form
        args['fee_form'] = fee_form
        args['roomDetail_form'] = roomDetail_form
        args['image_form'] = image_form
        args['hostel'] = Hostel.objects.get(id=pk)

        return render(request,'webpage/hostel_edit.html',args)

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
                   r.available=x['available']
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
        else:
            hostel_owner = HostelOwner.objects.get(user=user)

        return redirect("webpage:hostel_details",hostel_owner.hostel.pk)
    else:
        raise Http404('Page not found with user Id : '+ user_id)

def user_student(request,user_id):
    if 'user_id' in request.session  and int(user_id)==request.session['user_id']:
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
        args['avg_hostels'] = popular_hostel()
        return render(request, 'webpage/home_page.html',args)
    else:
        raise Http404('Page not found with user Id : ' + user_id)

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

        if Rating.objects.filter(hostel=hostel).exists():
            total_rating = 0
            rating_hostel = Rating.objects.filter(hostel=hostel)
            for rating in rating_hostel:
                total_rating = total_rating + rating.rating
            avg_rating = total_rating / len(rating_hostel)
        else:
            avg_rating = 0.0

        Rating.objects.filter(hostel=hostel).update(avg=avg_rating)

    return redirect("webpage:hostel_details",pk)