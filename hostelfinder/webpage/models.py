from django.db import models
from hostelAdmin.models import Hostel

class User(models.Model):
    USER_TYPE_CHOICE = {
        ('O','Hostel_Owner'),
        ('S', 'Student'),
    }
    first_name =  models.CharField(max_length=250)
    last_name =  models.CharField(max_length=250)
    user_name =  models.CharField(max_length=250)
    password =  models.CharField(max_length=250)
    email =  models.CharField(max_length=250)
    contact =  models.CharField(max_length=250)
    user_type =  models.CharField(max_length=20, choices=USER_TYPE_CHOICE)

    def __str__(self):
        return str(self.user_name) + ' - ' + str(self.pk)

class HostelOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

class Student(models.Model):
    GENDER_CHOICE = {
        ('M', 'Male'),
        ('F', 'Female'),
    }
    institute =  models.CharField(max_length=250)
    gender =  models.CharField(max_length=25, choices= GENDER_CHOICE)
    date_of_birth =  models.DateField()
