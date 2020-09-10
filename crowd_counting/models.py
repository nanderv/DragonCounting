import datetime

from django.db import models


# Create your models here.

class CrowdStatus(models.Model):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField(null=True, blank=True)
    crowd = models.IntegerField()

    @staticmethod
    def set_status(crowd: int):
        statuses = CrowdStatus.objects.filter(to_datetime=None)
        print("Z")
        if len(statuses) == 0:
            CrowdStatus.objects.create(from_datetime=datetime.datetime.now(), crowd=crowd)
        else:
            status = statuses[0]
            if status.crowd != crowd:
                status.to_datetime = datetime.datetime.now()
                status.save()
                CrowdStatus.objects.create(from_datetime=datetime.datetime.now(), crowd=crowd)
