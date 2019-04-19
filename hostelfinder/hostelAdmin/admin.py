from django.contrib import admin
from .models import Hostel, Room, Location, Fee, Image

admin.site.register(Location)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Fee)
admin.site.register(Image)