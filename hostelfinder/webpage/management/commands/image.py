from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Room, Fee, Image
import random
import csv

def generate_random_profile_image_int():
    no = random.randint(1,6)
    return no

def generate_random_kitchen_int():
    no = random.randint(1,7)
    return no

def generate_random_room_int():
    no = random.randint(1,11)
    return no

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        for hostel in Hostel.objects.all() :
            image = Image.objects.filter(hostel=hostel).update(
                profile_image = 'hostel'+str(generate_random_profile_image_int())+'.jpg',
                hostel_image = 'hostel'+str(generate_random_profile_image_int())+'.jpg',
                kitchen = 'kitchen'+str(generate_random_kitchen_int())+'.jpg',
                room = 'room'+str(generate_random_room_int())+'.jpg'
            )