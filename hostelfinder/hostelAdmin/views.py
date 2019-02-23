from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Hostel, Location, Geography

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

class HostelCreate(generic.CreateView):
    model = Hostel
    fields = ['hostel_name','hostel_type','hostel_phone','hostel_mobile']


def customers(request):
    all_hostels = Hostel.objects.all()
    return render(request,'hostelAdmin/customers.html', {"all_hostels" : all_hostels})