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
    email =  models.EmailField(max_length=250,null=True,blank=True)
    contact =  models.CharField(max_length=250,null=True,blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute =  models.CharField(max_length=250)
    gender =  models.CharField(max_length=25, choices= GENDER_CHOICE)
    date_of_birth =  models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.user)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    avg = models.DecimalField(max_digits=20,decimal_places=1,default="0.0")

    def __str__(self):
        return str(self.user) + ' - ' + str(self.hostel) + ' - ' + str(self.rating)

    # def save(self, *args, **kwargs):
    #     hostel = Hostel.objects.get(id=self.hostel_id)
    #
    #     if Rating.objects.filter(hostel=hostel).exists():
    #         total_rating = 0
    #         rating_hostel = Rating.objects.filter(hostel=hostel)
    #         for rating in rating_hostel:
    #             total_rating = total_rating + rating.rating
    #         avg_rating = total_rating / len(rating_hostel)
    #     else:
    #         avg_rating = 0.0
    #     print(avg_rating)
    #     Rating.objects.filter(hostel=hostel).update(avg=avg_rating)
    #     self.avg = avg_rating
    #     super(Rating, self).save(*args, **kwargs)