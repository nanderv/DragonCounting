from django.contrib import admin

# Register your models here.
from reservations.models import Timeslot, Reservation

admin.site.register(Timeslot)
admin.site.register(Reservation)