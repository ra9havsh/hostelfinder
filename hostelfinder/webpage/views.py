from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from .forms import RegistrationForm, StudentForm, LogInForm, SearchForm
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from hostelAdmin.forms import HostelForm, RoomForm, FeeForm, RoomDetailForm, ImageForm
from webpage.models import User, HostelOwner, Student, Rating
import json
import math
import requests
from django.conf import settings
import os

def haversine(hostel,latitude,longitude):
    R = 6372800  # Earth radius in meters
    diff_latitude = latitude-float(hostel.latitude)
    diff_longitude = longitude-float(hostel.longitude)

    phi1, phi2 = math.radians(hostel.latitude), math.radians(latitude)
    dphi = math.radians(diff_latitude)
    dlambda = math.radians(diff_longitude)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # diff_latitude = float(hostel.latitude)-latitude
    # diff_longitude = float(hostel.longitude)-longitude
    # e = math.sqrt((diff_latitude*diff_latitude) + (diff_longitude*diff_longitude))
    # print(f'{hav}-{hostel.location.street}-{hostel.hostel_name}')

def near_hostel(student_institute,similar_hostels):
    # file = os.path.join(settings.BASE_DIR, 'webpage/static/webpage/location.json')
    # json_file = open(file)
    # results = json.load(json_file)
    # json_file.close()

    #get json response from google geocoder api using url
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    institute = student_institute + ', Kathmandu'
    params = {'sensor': 'false', 'address': institute,'key':'AIzaSyDJ5YrHe6GorQ8BVPtT_gsmTM6ElhZwEHY'}
    r = requests.get(url, params=params)
    results = r.json()
    
    location  = results['results'][0]['geometry']['location']
    latitude=location['lat']
    longitude=location['lng']
    near_hostel = []

    for hostel in similar_hostels:
        e = haversine(hostel, latitude, longitude)
        if e < 1000:
            near_hostel.append([hostel,e])

    if len(near_hostel):
        near_hostel.sort(key=lambda x: x[1])
        hostel = []
        for h in near_hostel:
            hostel.append(h[0])
        return hostel[:12]
    else:
        return 0

def popular_hostel():
    rating = Rating.objects.order_by('-avg').values_list('hostel','avg').distinct()[:9]
    hostel =[]
    for rating in rating:
        hostel.append(int(rating[0]))

    avg_hostel =[]
    for h in hostel:
        avg_hostel.append(Hostel.objects.get(id=h))
    # print(avg_hostel)
    return avg_hostel

def evaluate_cosine_similarity(user,similar_user):
    numerator = 0
    user_square_sum = 0
    similar_user_square_sum = 0

    for i in range(len(user)):
        numerator = numerator + (user[i]*similar_user[i])
        user_square_sum = user_square_sum + (user[i]*user[i])
        similar_user_square_sum = similar_user_square_sum + (user[i]*user[i])

    denominator = math.sqrt(user_square_sum) + math.sqrt(similar_user_square_sum)
    similarity = numerator/denominator
    return similarity

def predict_user_item_rating(user,similar_user,cosine_similarity):
    denominator = 0
    predictate_rating = []

    similar_user_average = []
    user_average = 0

    for i in range(len(cosine_similarity)):
        denominator = denominator + cosine_similarity[i]

    for i in range(len(similar_user)):
        average = 0;
        total = 0;
        for j in range(len(similar_user[0])):
            total = total + similar_user[i][j]
        average = total/len(similar_user[0])
        similar_user_average.append(average)

    total = 0
    for i in range(len(user)):
        total = total + user[i]
    user_average  = total/len(user)

    for j in range(len(similar_user[0])):
        numerator = 0
        for i in range(len(similar_user)):
            numerator = numerator + ((similar_user[i][j]-similar_user_average[i])*cosine_similarity[i])
        predict = user_average + (numerator/denominator)
        predictate_rating.append(predict)

    return predictate_rating

def similar_hostel(user_id):
    user_rated_hostel = []
    similar_rating_user_id = []
    similar_user_rated_hostels = []
    student = Student.objects.get(user_id=user_id)
    rating = Rating.objects.filter(user=student.user_id)

    if student.gender == 'M':
        hostel_type = 'B'
    else:
        hostel_type = 'G'

    #get the hostels rated by active user
    for rating in rating:
        user_rated_hostel.append(rating.hostel)

    #get the similar users who rated the hostels rated by active user
    similar_rating = Rating.objects.filter(hostel__in=user_rated_hostel,user__student__gender=student.gender).order_by('user_id').exclude(user_id=user_id)

    #prepare the list of similar rating users and the hostels they rated
    for s in similar_rating:
        similar_rating_user_id.append(s.user_id)

        for h in Rating.objects.filter(user_id=s.user_id,hostel__hostel_type='B'):
            similar_user_rated_hostels.append(h.hostel_id)

    hostel = []

    if similar_user_rated_hostels and similar_rating_user_id:
        # removing duplicates
        similar_rating_user_id = list(dict.fromkeys(similar_rating_user_id))
        similar_user_rated_hostels = list(dict.fromkeys(similar_user_rated_hostels))
        similar_rating_user_id.sort()
        similar_user_rated_hostels.sort()

        #create user-item matrix for both active user and similar users
        similar_user =  [[0] * len(similar_user_rated_hostels) for i in range(len(similar_rating_user_id))]
        user = []

        for i,similar_user_id in enumerate(similar_rating_user_id):
            for j,hostel_id in enumerate(similar_user_rated_hostels):
                if Rating.objects.filter(user_id=similar_user_id,hostel_id=hostel_id).exists():
                    r = Rating.objects.values('rating').get(user_id=similar_user_id,hostel_id=hostel_id)
                    rate = r['rating']
                else:
                   rate = 0
                similar_user[i][j] = rate


        for i, similar_user_id in enumerate(similar_rating_user_id):
            for j, hostel_id in enumerate(similar_user_rated_hostels):
                print(str(similar_user_id)+'-'+str(hostel_id)+"="+str(similar_user[i][j]))
            print()

        for j in similar_user_rated_hostels:
            if Rating.objects.filter(user_id=user_id, hostel_id=j).exists():
                r = Rating.objects.values('rating').get(user_id=user_id, hostel_id=j)
                rate = r['rating']
            else:
                rate = 0
            user.append(rate)

        print(user)

        #calculating similarity through cosine similarity
        cosine_similarity = []


        print("cosine similarity:")
        for i in range(len(similar_rating_user_id)):
            similarity = evaluate_cosine_similarity(user,similar_user[i])
            cosine_similarity.append(similarity)
            print(str(similar_rating_user_id[i])+'-'+str(round(similarity,3)))

        if cosine_similarity:
            #predicting the rating for the each item of active user
            predictate_rating = predict_user_item_rating(user,similar_user,cosine_similarity)

            print("predictate rating:")
            for i in range(len(similar_user_rated_hostels)):
                print((str(similar_user_rated_hostels[i])+'-'+str(round(predictate_rating[i],2))))

            #now finding the top predictate hostel rating
            predictate_similar_hostel = []
            hostels = []
            for j, hostel_id in enumerate(similar_user_rated_hostels):
                predictate_similar_hostel.append((hostel_id,predictate_rating[j]))
            predictate_similar_hostel.sort(key=lambda x  : x[1],reverse=True)

            print("ranked hostels")
            for p in predictate_similar_hostel:
                hostels.append(p[0])
                print(p[0])

            for h in hostels:
                hostel.append( Hostel.objects.get(id=h))

        # for h in hostel:
        #     print(h)

    return hostel[:9]

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

def search_bar(request):
    search_value = request.GET.get('search_value')
    print(search_value)

    searched= False
    hostel = Hostel.objects.all()

    if search_value:
        hostel = hostel.filter(hostel_name__icontains=search_value)
        searched = True

    if searched:
        paginator = Paginator(hostel, 18)  # Show 18 contacts per page
        page = request.GET.get('page')
        hostels = paginator.get_page(page)

        if 'user_id' in request.session:
            user_id = request.session['user_id']
            user = get_object_or_404(User, id=user_id)
            return render(request, 'webpage/search_result.html', {'hostels': hostels, 'username': user.user_name})
        else:
            return render(request, 'webpage/search_result.html', {'hostels': hostels})

    else:
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
    hostel = get_object_or_404(Hostel,id=pk)
    args = {}
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        rating_user = Rating.objects.filter(user_id=user_id,hostel_id=pk).exists()

        if rating_user:
            rating_user = get_object_or_404(Rating,user_id=user_id, hostel_id=pk)
            args = {'hostel': hostel, 'username': user.user_name,'rating_user':rating_user.rating}
        else:
            args = {'hostel':hostel,'username':user.user_name}

        if user.user_type=='O':
            args['hostel_owner']=True
    else:
        args = {'hostel':hostel}

    # args['avg_rating'] = avg_rating
    return render(request,'webpage/hostel_detail.html',args)

def HostelEditView(request, pk):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
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
        args['username'] = user.user_name
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

        # for popular hostel
        args['avg_hostels'] = popular_hostel()

        # for similar hostel
        student = Student.objects.get(user_id=user_id)
        if student.gender == 'M':
            hostel_type = 'B'
        else:
            hostel_type = 'G'

        if Rating.objects.filter(user_id=user_id,hostel__hostel_type=hostel_type).exists() :
            similar_hostels = []
            similar_hostels = similar_hostel(user_id)
            args['similar_hostels'] = similar_hostels

            # for near hostels
            student_institute = Student.objects.get(user_id=user_id).institute
            if near_hostel(student_institute,similar_hostels):
                args['near_hostels']=near_hostel(student_institute,similar_hostels)
                args['student_institute'] = student_institute

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