from django.db import models

# Create your models here.


class TempUrl(models.Model):
    code = models.CharField(max_length=64)