from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Location
from webpage.models import User, Student
import csv
import random
import requests


def nearest_hostel():
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': 'Trinity International College, kathmandu','key':'AIzaSyDJ5YrHe6GorQ8BVPtT_gsmTM6ElhZwEHY'}
    r = requests.get(url, params=params)
    results = r.json()
    print(results)

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        nearest_hostel()

