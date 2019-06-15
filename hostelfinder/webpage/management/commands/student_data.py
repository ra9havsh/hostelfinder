from django.core.management.base import BaseCommand
from webpage.models import User, HostelOwner, Student
import csv
import random

college = []

def generate_random_college():
    no = random.randint(0, len(college)-1)
    return str(college[no][0])

def generate_random_date_of_birth():
    m = random.randint(1,12)
    d = random.randint(1,28)
    y = random.randint(1880,2000)

    if m < 10:
        mm = str(0)+str(m)
    else:
        mm = str(m)

    if d < 10:
        dd= str(0)+str(d)
    else:
        dd = str(d)

    yy = str(y)

    return yy+'-'+mm+'-'+dd

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('user_file_name', type=str, help="hostel detail")
        parser.add_argument('college_file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        user_file_name = kwargs['user_file_name']
        college_file_name = kwargs['college_file_name']

        with open(f'{college_file_name}.csv', 'r') as file:
            college_csv_reader = csv.reader(file)
            next(college_csv_reader)

            for line in college_csv_reader:
                college.append(line)

        with open(f'{user_file_name}.csv','r') as file:
            user_csv_reader = csv.reader(file)
            next(user_csv_reader)
            for line in user_csv_reader:
                user = User.objects.create(
                      first_name = line[0],
                      last_name = line[1],
                      user_name = str(line[0]),
                      password = 'qwertyuiop',
                      email = line[2],
                      contact = line[3],
                      user_type = 'S'
                )

                if 'Male' in line[4]:
                    gender = 'M'
                else:
                    gender = 'F'

                student = Student.objects.create(
                    user = user,
                    institute = generate_random_college(),
                    gender = gender,
                    date_of_birth = generate_random_date_of_birth(),
                )

            user_name = []
            for s in User.objects.filter(user_type='S'):
                user_name.append(s.first_name+str(s.id))

            id = 0
            for u in User.objects.filter(user_type='S'):
                u.user_name=user_name[id]
                u.save()
                id=id+1


