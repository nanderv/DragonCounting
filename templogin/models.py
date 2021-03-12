from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class CrossLogin(models.Model):
    perms_level = models.IntegerField()
    user = models.ForeignKey(User,on_delete=CASCADE)