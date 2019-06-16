from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Location
from webpage.models import User, Student
import csv
import random


def nearest_hostel():
    student = Student.objects.values_list('institute').distinct()
    for student in student:
        print(student[0])

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        nearest_hostel()

