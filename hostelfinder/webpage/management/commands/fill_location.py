from django.core.management.base import BaseCommand
from hostelAdmin.models import Location
import csv

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.csv','r') as file:
            loc_list = []
            csv_reader = csv.reader(file)
            next(csv_reader)

            for line in csv_reader :
                loc_list.append(line[3])

            loc_list = list(dict.fromkeys(loc_list))

            for location in loc_list:
                location = Location.objects.create(
                    street = location
                )