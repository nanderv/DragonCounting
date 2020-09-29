from django.db import models
from datetime import date

# Create your models here.
from django.utils.functional import lazy


FULL_LIST = [('afternoon', 'Afternoon'), ('evening', 'Evening'), ('writing', 'Writing Evening')]
def get_choices():
    return [('afternoon', 'Afternoon'), ('evening', 'Evening')]


class Reservation(models.Model):
    timeslot = models.CharField(choices=FULL_LIST, max_length=64)
    name = models.CharField(max_length=16)
    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Reservation.objects.filter(date__lt=date.today())

        lst.delete()
