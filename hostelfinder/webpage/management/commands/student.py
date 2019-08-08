from django.core.management.base import BaseCommand
from webpage.models import User, HostelOwner, Student
import csv
import random

college = []

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('user_file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        user_file_name = kwargs['user_file_name']

        with open(f'{user_file_name}.csv','r') as file:
            user_csv_reader = csv.reader(file)
            next(user_csv_reader)
            for line in user_csv_reader:

                student_name = line[1].split();
                first_name = student_name[0]
                last_name = student_name[len(student_name) - 1]

                user = User.objects.create(
                      first_name = first_name,
                      last_name = last_name,
                      user_name = str(line[1]),
                      password = 'qwertyuiop',
                      email = line[0],
                      contact = None,
                      user_type = 'S'
                )
                print(user)
                if 'Male' in line[2]:
                    gender = 'M'
                else:
                    gender = 'F'

                student = Student.objects.create(
                    user = user,
                    institute = line[3],
                    gender = gender,
                    date_of_birth = None
                )

            user_name = []
            for s in User.objects.filter(user_type='S'):
                user_name.append(s.first_name+str(s.id))

            id = 0
            for u in User.objects.filter(user_type='S'):
                u.user_name=user_name[id]
                u.save()
                id=id+1


