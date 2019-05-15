from django.contrib import admin
from .models import User, HostelOwner, Student

admin.site.register(User)
admin.site.register(HostelOwner)
admin.site.register(Student)
