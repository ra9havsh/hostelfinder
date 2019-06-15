from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel
from webpage.models import Student, Rating, User
import random
import csv

def generate_random_int():
    no = random.randint(8, 18)
    return no

def generate_random_student_int():
    no = random.randint(Student.objects.first().user.id, Student.objects.last().user.id)
    return no

def generate_random_rating_int():
    no = random.randint(1, 5)
    return no

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        for hostel in Hostel.objects.all() :
            log = []
            for i in range(generate_random_int()):
                student = generate_random_student_int()

                if student in log:
                    i=i-1
                    continue
                else:
                    log.append(student)

                rating = Rating.objects.create(
                    hostel = hostel,
                    user = User.objects.get(id=generate_random_student_int()),
                    rating = generate_random_rating_int()
                )