from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views import generic
from .models import Hostel, Location, Room, Fee, Image
from .forms import HostelForm, RoomForm, FeeForm, RoomDetailForm, ImageForm
from django.contrib import messages
import json

def HostelView(request):
    hostel_list = Hostel.objects.all()
    location = Location.objects.all()

    paginator = Paginator(hostel_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    hostel = paginator.get_page(page)
    return render(request, 'hostelAdmin/hostels.html', {'hostels': hostel, 'locations':location})

def HostelDetailView(request, pk):
    hostel = Hostel.objects.get(id=pk)
    args = {'hostel':hostel}
    return render(request,'hostelAdmin/hostel_detail.html',args)


def HostelEditView(request, pk):
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
                    r.available=x['available']
                    r.save()

            room.hostel =hostel
            fee.hostel = hostel
            image.hostel = hostel
            fee.save()
            image.save()

            return redirect("hostelAdmin:hostel_details",pk=pk)

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

    return render(request,'hostelAdmin/hostel_edit.html',args)


#class HostelCreate(generic.CreateView):
 #  model = Hostel
 #  fields = ['hostel_name','hostel_type','hostel_phone','hostel_mobile']

def formHostel(request):
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

            return redirect("hostelAdmin:hostels")

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

    return render(request,'hostelAdmin/new_hostel.html',args)

def HostelDeleteView(request,pk):
    hostel = get_object_or_404(Hostel, id=pk)
    try:
        if request.method == "POST" and request.user.is_authenticated:
            print("fa")
            hostel.delete()
            messages.success(request, "Post successfully deleted!")
            return redirect("hostelAdmin:hostels")
    except Exception as e:
        messages.warning(request,"could not delete: Error {}".format(e))

    args = {'hostel': hostel}

    return render(request,'hostelAdmin/hostel_detail.html',args)

def customers(request):
    return render(request,'hostelAdmin/customers.html')
