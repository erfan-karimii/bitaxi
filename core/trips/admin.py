from django.contrib import admin
from .models import Trips, DriverOffers, Comment

# Register your models here.

admin.site.register(Trips)
admin.site.register(Comment)
admin.site.register(DriverOffers)
