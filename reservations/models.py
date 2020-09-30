from django.db import models
from datetime import date, timedelta

# Create your models here.
from django.db.models import CASCADE
from django.utils.functional import lazy


def get_slots_is_open(slot_name, date_to_measure: date):
    if slot_name == 'afternoon' or slot_name == 'evening':
        return date_to_measure.isoweekday() < 6
    if slot_name == 'writing':
        return date_to_measure.isoweekday() == 3


class TimeslotManager(models.Manager):
    def only_current(self):
        reservations = Reservation.objects.filter(date=date.today())
        # Count reservations
        res = dict()
        for reservation in reservations:
            res[reservation.timeslot] = res.get(reservation.timeslot, 0) + 1

        # Set exclusion list
        excl = []
        for z in res.keys():
            if res[z] >= z.capacity:
                excl.append(z.pk)

        # Final query
        iso_day = str(date.today().isoweekday())
        return self.model.objects.filter(on_day__contains=iso_day).exclude(pk__in=excl)


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
    timeslot = models.ForeignKey(Timeslot, on_delete=CASCADE)
    name = models.CharField(max_length=16)
    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Reservation.objects.filter(date__lt=date.today() - timedelta(days=1))
        lst.delete()

    def __str__(self):
        return str(self.date) + "::" + str(self.timeslot) + " : " + self.name
