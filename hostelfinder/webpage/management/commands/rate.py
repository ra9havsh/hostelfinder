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
        user_file_name = kwargs['user_file_name']

        with open(f'{user_file_name}.csv','r') as file:
            user_csv_reader = csv.reader(file)
            next(user_csv_reader)

            with open('rate.csv', mode='w',newline='') as rate_file:
                rate_writer = csv.writer(rate_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                rate_writer.writerow(['user', 'hostel', 'rating'])

                for line in user_csv_reader:
                    user = User.objects.get(email__icontains=line[0])
                    hostel1_name = None
                    hostel2_name = None
                    hostel3_name = None
                    rate1 = None
                    rate2= None
                    rate3 = None


                    if line[4]!='' and Hostel.objects.filter(hostel_name__icontains=line[4]).exists():
                        hostel1= Hostel.objects.filter(hostel_name__icontains=line[4]).first()
                        hostel1_name = hostel1.hostel_name

                    if line[6]!='' and Hostel.objects.filter(hostel_name__icontains=line[6]).exists():
                        hostel2 = Hostel.objects.filter(hostel_name__icontains=line[6]).first()
                        hostel2_name = hostel2.hostel_name

                    if line[8]!='' and Hostel.objects.filter(hostel_name__icontains=line[8]).exists():
                        hostel3= Hostel.objects.filter(hostel_name__icontains=line[8]).first()
                        hostel3_name = hostel3.hostel_name

                    if line[5]!='':
                        rate1 = str(line[5])

                    if line[7]!='':
                        rate2 = str(line[7])

                    if line[9]!='':
                        rate3 = str(line[9])

                    if hostel1_name is not None and rate1 is not None:
                        rate_writer.writerow([str(user.id),str(hostel1_name),str(rate1)])
                        print(str(user.id) + '-' + str(hostel1_name) + '-' + str(rate1))

                        Rating.objects.create(
                            hostel=hostel1,
                            user=user,
                            rating=rate1
                        )

                    if hostel2_name is not None and rate2 is not None:
                        rate_writer.writerow([str(user.id), str(hostel2_name), str(rate2)])
                        print(str(user.id) + '-' + str(hostel2_name) + '-' + str(rate2))

                        Rating.objects.create(
                            hostel=hostel2,
                            user=user,
                            rating=rate2
                        )

                    if hostel3_name is not None and rate3 is not None:
                        rate_writer.writerow([str(user.id), str(hostel3_name), str(rate3)])
                        print(str(user.id) + '-' + str(hostel3_name) + '-' + str(rate3))

                        Rating.objects.create(
                            hostel=hostel3,
                            user=user,
                            rating=rate3
                        )

                    #print(str(user.id)+'-'+str(hostel1_name)+'-'+str(rate1)+'-'+str(hostel2_name)+str(rate2)+'-'+str(hostel3_name)+'-'+str(rate3))




