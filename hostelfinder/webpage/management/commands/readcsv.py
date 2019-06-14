from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Room, Location, Fee, Image
from webpage.models import User, HostelOwner
import csv
import random


def generate_hostel_type(hostel_name):
    if "boy" in hostel_name.lower():
       return 'B'
    else:
       return 'G'


class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.csv','r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader :
                hostel = Hostel.objects.create(
                    hostel_name = line[2],
                    hostel_type = generate_hostel_type(line[2]),
                    hostel_mobile = line[0],
                    latitude = float(line[4]),
                    longitude= float(line[5]),
                    location = Location.objects.get(street=line[3]),
                    additional_location = line[6]
                )

                owner_name = line[1].split();
                first_name = owner_name[0]
                last_name = owner_name[len(owner_name) - 1]
                user_name = first_name + str(hostel.pk)
                password = "qwertyuiop"

                user = User.objects.create(
                          first_name = first_name,
                          last_name = last_name,
                          user_name = user_name,
                          password = password,
                          contact = line[0],
                          user_type = 'O'
                  )

                hostel_owner = HostelOwner.objects.create(hostel=hostel,user=user)

            Hostel.objects.filter(additional_location='').update(additional_location=None)


