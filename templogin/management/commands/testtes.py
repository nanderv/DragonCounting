import http.client
import string
import random
from django.core.management.base import BaseCommand

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

from bellettrie_library_system.cross_login import my_encrypt, my_decrypt, MemberData


class Command(BaseCommand):
    help = 'Set the traffic light'

    def handle(self, *args, **options):
        d = my_encrypt(MemberData("Nander", 873, 2))
        print(d)
        print(my_decrypt(d))
