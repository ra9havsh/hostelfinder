from django.shortcuts import render
from .forms import HostelOwnerRegistration
#from hostelAdmin.models import Hostel, Location, Room, Fee, Image

def homepage(request):
    return render(request,'webpage/home_page.html')

def register_view(request):
    return render(request,'webpage/register.html')
2
def register_form_view(request):
    form = HostelOwnerRegistration()
    return render(request,'webpage/register_form.html',{'form':form})