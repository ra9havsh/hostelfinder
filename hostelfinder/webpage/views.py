from django.shortcuts import render

def homepage(request):
    return render(request,'webpage/home_page.html')

def register_view(request):
    return render(request,'webpage/register.html')