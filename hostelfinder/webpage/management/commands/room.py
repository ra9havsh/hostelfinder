from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Room, Fee, Image
import random
import csv


def generate_random_int():
    no = random.randint(3, 5)
    return no * 'a'

def generate_random_quantity_int():
    no = random.randint(2,3)
    return no

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        for hostel in Hostel.objects.all() :
            for i in generate_random_int():


                room = Room.objects.create(
                    hostel = hostel,
                    seater_type
                    quantity
                    room_price
                )
