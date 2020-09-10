import datetime

from django.db import models

# Create your models here.
class TrafficLightStatus(models.Model):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField(null=True, blank=True)
    open = models.BooleanField()

    @staticmethod
    def set_status(open:bool):
        statuses = TrafficLightStatus.objects.filter(to_datetime=None)
        status = None
        if len(statuses) == 0:
            TrafficLightStatus.objects.create(from_datetime=datetime.datetime.now(), open=open)
        else:
            status = statuses[0]
            if status.open != open:
                status.to_datetime =datetime.datetime.now()
                status.save()
                TrafficLightStatus.objects.create(from_datetime=datetime.datetime.now(), open=open)
