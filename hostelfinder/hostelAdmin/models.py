from django.db import models
from django.urls import reverse

class Location(models.Model):
    city = models.CharField(max_length=250)
    street = models.CharField(max_length=250, default="Kathmandu")
    province = models.IntegerField(default=3)
    zip = models.CharField(max_length=250)
    country = models.CharField(max_length=250, default="Nepal")

    def __str__(self):
        return str(self.pk)+' : '+self.city + ' - '+self.street

class Hostel(models.Model):
    HOSTEL_CHOICE = {
        ('B','Boys Hostel'),
        ('G', 'Girls Hostel'),
    }
    hostel_name =  models.CharField(max_length=250)
    hostel_type =  models.CharField(max_length=20, choices=HOSTEL_CHOICE)
    hostel_phone =  models.CharField(max_length=100)
    hostel_mobile = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('hostelAdmin:hostel_details', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.pk)+' - '+self.hostel_name + '('+  self.hostel_type +')'


class Geography(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, default=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    latitude = models.DecimalField(max_digits=10,decimal_places=8, default=0.000000)
    longitude = models.DecimalField(max_digits=11,decimal_places=8, default=0.00000)
    additional = models.CharField(max_length=250)


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    seater_type= models.IntegerField(default=1)
    quantity = models.IntegerField(default=1)
    room_price = models.CharField(max_length=250)

    def __str__(self):
        return str(self.hostel.pk)+' : '+self.hostel.hostel_name + ' - room'+  str(self.pk) +')'

class Fee(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    admission_fee = models.CharField(max_length=250)
    refundable_fee = models.CharField(max_length=250)
    security_fee = models.CharField(max_length=250)

    def __str__(self):
        return str(self.hostel.pk)+' : '+self.hostel.hostel_name + ' fee'

class Image(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=250)
    image1 = models.CharField(max_length=250, default="n/a")
    image2 = models.CharField(max_length=250, default="n/a")
    image3 = models.CharField(max_length=250, default="n/a")
    image4 = models.CharField(max_length=250, default="n/a")
    image5 = models.CharField(max_length=250, default="n/a")

    def __str__(self):
        return str(self.hostel.pk)+' : '+self.hostel.hostel_name + ' images'
