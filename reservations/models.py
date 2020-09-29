from django.db import models
from datetime import date, timedelta

# Create your models here.
from django.db.models import CASCADE
from django.utils.functional import lazy

FULL_LIST = [('afternoon', 'Afternoon'), ('evening', 'Evening'), ('writing', 'Writing Evening')]
SLOT_CAPACITIES = {'afternoon': 10, 'evening': 10, 'writing': 10}


def get_slots_is_open(slot_name, date_to_measure: date):
    if slot_name == 'afternoon' or slot_name == 'evening':
        return date_to_measure.isoweekday() < 6
    if slot_name == 'writing':
        return date_to_measure.isoweekday() == 3


class TimeslotManager(models.Manager):
    def only_current(self):
        from django.db import connection
        result_list = []
        timeslots = self.model.objects.all()
        for timeslot in timeslots:
             if timeslot.is_on_today() and timeslot.get_len_res() < timeslot.capacity:
                 result_list.append(timeslot.pk)
        return self.model.objects.filter(pk__in=result_list)

class Timeslot(models.Model):
    name = models.CharField(max_length=32)
    on_day = models.CharField(max_length=7)
    capacity = models.IntegerField()
    objects = TimeslotManager()

    def is_on_today(self):
        return str(date.today().isoweekday()) in self.on_day

    def get_reservations(self):
        return Reservation.objects.filter(timeslot=self, date=date.today())

    def get_len_res(self):
        return len(self.get_reservations())

    def __str__(self):
        return self.name


class Reservation(models.Model):
    timeslot = models.ForeignKey(Timeslot,on_delete=CASCADE)
    name = models.CharField(max_length=16)
    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Reservation.objects.filter(date__lt=date.today() - timedelta(days=28))
        lst.delete()

    def __str__(self):
        return str(self.date)+"::"+ str(self.timeslot) + " : " + self.name


class Register(models.Model):
    name = models.CharField(max_length=16)
    email = models.CharField(max_length=128)

    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Register.objects.filter(date__lt=date.today() - timedelta(days=28))
        lst.delete()
