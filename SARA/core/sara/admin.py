from django.contrib import admin

# Register your models here.
from .models import Records, Rooms

admin.site.register(Records)
admin.site.register(Rooms)