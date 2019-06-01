from django.contrib import admin
from .models import User, HostelOwner, Student, Rating

admin.site.register(User)
admin.site.register(HostelOwner)
admin.site.register(Student)
admin.site.register(Rating)
