from django.contrib import admin

# Register your models here.
from reservations.models import Timeslot, Reservation, Register

admin.site.register(Timeslot)
admin.site.register(Reservation)
admin.site.register(Register)