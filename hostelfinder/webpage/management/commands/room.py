from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Room, Fee, Image
import random
import csv

room = [[3,1500],[3,2000],[2,1500],[2,1200],[1,4000],[1,3000],[1,2500]]

def generate_random_int():
    no = random.randint(3, 4)
    return no

def generate_random_quantity_int():
    no = random.randint(2,3)
    return no

def generate_random_seater_int():
    no = random.randint(0,len(room)-1)
    return no

def generate_random_available_int():
    no = random.randint(0,3)
    return no

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        room_arr = [[3, 1500], [3, 2000], [2, 1500], [2, 1200], [1, 4000], [1, 3000], [1, 2500]]
        admission_fee = [5000,10000,12000,4000,4500,8000]
        refundable_fee = [1000,2000,3000,1000,1000,1000]
        security_fee = [1000,20000,3000,1000,1000,1000]

        for hostel in Hostel.objects.all() :

            log = []
            for i in range(generate_random_int()):
                seater = generate_random_seater_int()
                avl = generate_random_available_int()
                quantity = generate_random_quantity_int()

                if seater in log:
                    i=i-1
                    continue
                log.append(seater)

                if avl == 0:
                    available=0
                elif avl == 1:
                    available = 1
                elif avl == 2:
                    available = quantity-1
                else:
                    available = quantity

                seater_type = room_arr[seater][0]
                room_price = str(room_arr[seater][1])

                room = Room.objects.create(
                    hostel = hostel,
                    seater_type = seater_type,
                    quantity = quantity,
                    room_price = room_price,
                    available = available
                )

            fee_count = random.randint(0,len(admission_fee)-1)
            fee = Fee.objects.create(
                hostel = hostel,
                admission_fee= admission_fee[fee_count],
                refundable_fee= refundable_fee[fee_count],
                security_fee = security_fee[fee_count]
            )