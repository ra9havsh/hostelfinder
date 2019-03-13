from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .models import Hostel, Location, Geography, Room, Fee
from .forms import HostelForm, GeographyForm, RoomForm, FeeForm, RoomDetailForm
import json

class HostelView(generic.TemplateView):
    template_name = 'hostelAdmin/hostels.html'

    hostels = Hostel.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HostelView, self).get_context_data(**kwargs)
        context['hostels'] = Hostel.objects.all()
        context['geo'] = Geography.objects.all()
        context['locations'] = Location.objects.all()
        return context

class HostelDetailView(generic.DetailView):
    model = Hostel
    template_name= 'hostelAdmin/hostel_detail.html'

#class HostelCreate(generic.CreateView):
 #  model = Hostel
 #  fields = ['hostel_name','hostel_type','hostel_phone','hostel_mobile']

def formHostel(request):
    if request.method == "POST":
        hostel_form = HostelForm(request.POST)
        geography_form = GeographyForm(request.POST)
        room_form = RoomForm(request.POST)
        fee_form = FeeForm(request.POST)
        roomDetail_form = RoomDetailForm(request.POST)

        if hostel_form.is_valid() and geography_form.is_valid() and fee_form.is_valid():
            hostel = hostel_form.save()
            geography = geography_form.save(False)
            room = room_form.save(False)
            fee = fee_form.save(False)
            data = json.loads(roomDetail_form.data['room_detail'])
            print(data[0]['room_price'])
            geography.hostel = hostel
            room.hostel =hostel
            fee.hostel = hostel
            geography.save()
            fee.save()

            return redirect("hostelAdmin:hostels")

    else:
        hostel_form = HostelForm()
        geography_form = GeographyForm()
        room_form = RoomForm()
        fee_form = FeeForm()
        roomDetail_form = RoomDetailForm()

    args = {}
    #args.update(csrf(request))
    args['hostel_form'] = hostel_form
    args['geography_form'] = geography_form
    args['room_form'] = room_form
    args['fee_form'] = fee_form
    args['roomDetail_form'] = RoomDetailForm()

    return render(request,'hostelAdmin/new_hostel.html',args)

def customers(request):
    pass