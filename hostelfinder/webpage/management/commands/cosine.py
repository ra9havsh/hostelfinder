from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Location
from webpage.models import User, Student, Rating
import csv
import random


def similar_hostel():
    rated_hostel = []
    student = Student.objects.get(user_id=4013)
    rating = Rating.objects.filter(user=student.user_id)
    for rating in rating:
        rated_hostel.append(rating.hostel)

    similar_rating_student = Rating.objects.filter(hostel__in=rated_hostel).order_by('user_id').exclude(user_id=4013)
    for s in similar_rating_student:
        print(s)

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        similar_hostel()

