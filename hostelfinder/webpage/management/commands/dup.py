from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Image
from webpage.models import Student, Rating, User
import random
import csv

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help="hostel detail")

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.csv', 'r') as file:
            csv_reader = csv.reader(file)

            for hostel in Hostel.objects.all():
                line=next(csv_reader)
                image = Image.objects.filter(hostel=hostel).update(
                    profile_image=line[0],
                    hostel_image=line[0]
                )
