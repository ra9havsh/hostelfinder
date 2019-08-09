from django.core.management.base import BaseCommand
from webpage.models import User, HostelOwner, Student, Rating
from hostelAdmin.models import Hostel
import csv
import random

college = []

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('user_file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        test_data = kwargs['user_file_name']

        with open(f'{test_data}.csv','r') as file:
            test_data_reader = csv.reader(file)
            next(test_data_reader)