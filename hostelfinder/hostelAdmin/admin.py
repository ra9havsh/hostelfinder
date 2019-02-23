from django.contrib import admin
from .models import Hostel, Room, Location, Geography, Fee, Image

admin.site.register(Location)
admin.site.register(Geography)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Fee)
admin.site.register(Image)