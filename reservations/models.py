from django.db import models
from datetime import date, timedelta, datetime

# Create your models here.
from django.db.models import CASCADE
from django.utils.functional import lazy


class TimeslotManager(models.Manager):
    def only_current(self, dt=None):

        if dt is None:
            dt = date.today()
        reservations = Reservation.objects.filter(date=dt)
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
        iso_day = str(dt.isoweekday())
        return self.model.objects.filter(on_day__contains=iso_day).exclude(pk__in=excl)

    def available_on_day(self, day=None, only_non_empty=False, also_before=False):
        # return []
        if day is None:
            day = date.today()

            print("TD")
        tss = self.only_current(day)
        tsz = tss
        if day == date.today():
            tsz = []
            for t in tss:
                print(datetime.now().time())
                print(t.ending_time)
                print(datetime.now().time() < t.ending_time)
                if datetime.now().time() < t.ending_time or also_before:
                    tsz.append(t)
        print(tsz)
        tss = tsz
        if not only_non_empty:
            return tss
        result = []
        for ts in tss:
            if len(Reservation.objects.filter(date=day, timeslot=ts)) > 0 or ts.is_forced_open_date(day):
                result.append(ts.pk)
        return self.model.objects.filter(pk__in=result)


class Timeslot(models.Model):
    name = models.CharField(max_length=32)
    on_day = models.CharField(max_length=7)
    capacity = models.IntegerField()
    objects = TimeslotManager()
    starting_time = models.TimeField(null=True)
    ending_time = models.TimeField(null=True)
    always_open = models.BooleanField(default=False)

    def is_on_days_future(self, d):
        print(d, (date.today()+timedelta(days=d)).isoweekday())
        return str((date.today()+timedelta(days=d)).isoweekday()) in self.on_day

    def is_on_today(self):
        return str(date.today().isoweekday()) in self.on_day

    def get_reservations_future(self, d):
        return Reservation.objects.filter(timeslot=self, date=date.today()+timedelta(days=d))

    def get_reservations(self):
        return Reservation.objects.filter(timeslot=self, date=date.today())

    def get_len_res(self):
        return len(self.get_reservations())

    def __str__(self):
        return self.name

    def get_options(self):
        return TimeslotOption.objects.filter(timeslot=self).order_by('name')

    def is_forced_open(self, days=0):
        date = datetime.today() + timedelta(days=days)

        return  self.always_open or  len(ForceOpen.objects.filter(timeslot=self,date=date))>0

    def is_forced_open_date(self, date):
        return  self.always_open or len(ForceOpen.objects.filter(timeslot=self,date=date))>0


class TimeslotOption(models.Model):
    name = models.CharField(max_length=32)
    timeslot = models.ForeignKey(Timeslot, on_delete=CASCADE)
    only_one = models.BooleanField(default=False)
    capacity = models.IntegerField(default=-1)

    def used_capacity(self):
        return  len(self.timeslotoptionvalue_set.all())

    def __str__(self):
        return self.name


def name_str_to_name(name_str):
    return name_str.split("@@")[0]


def name_str_to_id(name_str):
    if len(name_str.split("@@")) > 1:
        return name_str.split("@@")[1]
    else:
        return ""


class Reservation(models.Model):
    timeslot = models.ForeignKey(Timeslot, on_delete=CASCADE)
    name = models.CharField(max_length=128)
    my_id = models.IntegerField(null=True, blank=True)
    date = models.DateField()

    @staticmethod
    def wipe():
        lst = Reservation.objects.filter(date__lt=date.today() - timedelta(days=1))
        lst.delete()
        lst = ForceOpen.objects.filter(date__lt=date.today() - timedelta(days=1))
        lst.delete()

    def __str__(self):
        return str(self.date) + "::" + str(self.timeslot) + " : " + self.name

    def get_options(self):
        return TimeslotOptionValue.objects.filter(reservation=self).order_by('timeslot_option__name')

    def get_name(self):
        return name_str_to_name(self.name)

    def get_id(self):
        return self.my_id


class TimeslotOptionValue(models.Model):
    timeslot_option = models.ForeignKey(TimeslotOption, on_delete=CASCADE)
    value = models.BooleanField()
    reservation = models.ForeignKey(Reservation, on_delete=CASCADE)


class ForceOpen(models.Model):
    timeslot = models.ForeignKey(Timeslot, on_delete=CASCADE)
    date = models.DateField()