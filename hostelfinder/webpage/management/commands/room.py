from django.core.management.base import BaseCommand
from hostelAdmin.models import Room
import csv


class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.csv','r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader :
                room = Room.objects.create(
                    hostel
                    seater_type
                    quantity
                    room_price
                )
