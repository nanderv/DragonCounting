import http.client
import string
import random
from django.core.management.base import BaseCommand

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

from templogin.models import TempUrl


class Command(BaseCommand):
    help = 'Set the traffic light'

    def handle(self, *args, **options):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(64))
        TempUrl.objects.create(code=result_str)
        print(result_str)
