from django.db import models
from datetime import date, timedelta

# Create your models here.
from django.utils.functional import lazy

FULL_LIST = [('afternoon', 'Afternoon'), ('evening', 'Evening'), ('writing', 'Writing Evening')]
SLOT_CAPACITIES = {'afternoon': 10, 'evening': 10, 'writing': 10}


class Reservation(models.Model):
    timeslot = models.CharField(choices=FULL_LIST, max_length=64)
    name = models.CharField(max_length=16)
    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Reservation.objects.filter(date__lt=date.today() - timedelta(days=28))
        lst.delete()


class Register(models.Model):
    name = models.CharField(max_length=16)
    email = models.CharField(max_length=128)

    date = models.DateField()
    @staticmethod
    def wipe():
        lst = Register.objects.filter(date__lt=date.today() - timedelta(days=28))
        lst.delete()