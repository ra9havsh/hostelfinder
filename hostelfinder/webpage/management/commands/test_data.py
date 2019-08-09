from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel
from webpage.models import Student, Rating, User
import random
import csv

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        with open('data.csv', mode='w', newline='') as rate_file:
            test_data_writer = csv.writer(rate_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            hostels = []
            users = []
            for hostel in Rating.objects.order_by('hostel').values('hostel').distinct() :
                hostel = Hostel.objects.get(id=hostel['hostel']);
                hostels.append(hostel)

            for student in Rating.objects.order_by('user').values('user').distinct() :
                user = User.objects.get(id=student['user']);
                users.append(user)

            header = []
            header.append('rating')
            for h in hostels:
                header.append(h.id)
            test_data_writer.writerow(header)

            for u in users:
                rate=[]
                rate.append(u.id)
                for h in hostels:
                    if Rating.objects.filter(hostel=h,user=u).exists():
                        r=Rating.objects.filter(hostel=h,user=u).first()
                        rate.append(r.rating)
                    else:
                        r=None
                        rate.append('0')
                    print(r)
                test_data_writer.writerow(rate)
