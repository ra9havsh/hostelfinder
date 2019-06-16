from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from webpage.models import User, HostelOwner, Rating
import csv
import random

def popular_hostel():
    rating = Rating.objects.values_list('hostel','avg').order_by('-avg').distinct()
    hostel =[]
    for rating in rating:
        print(str(rating[0]))
        hostel.append(int(rating[0]))

    avg_hostel = Hostel.objects.filter(id__in=hostel)[:18]
    print(avg_hostel)

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        popular_hostel()

