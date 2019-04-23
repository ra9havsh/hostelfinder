from django.shortcuts import render

def homepage(request):
    return render(request,'webpage/hostel_detail.html')