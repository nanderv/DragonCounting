import http.client
from django.core.management.base import BaseCommand

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

from traffic_light.models import TrafficLightStatus


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


URL = 'http://baliepc.student.utwente.nl:8080/green.png'


class Command(BaseCommand):
    help = 'Set the traffic light'

    def handle(self, *args, **options):
        open = False
        import urllib.request
        import urllib.error
        try:
            try:
                f = urllib.request.urlopen(URL, timeout=5)
                if f.status == 200 or f.status == 302:
                    open = True
                else:
                    print("DK Closed")
            except urllib.error.HTTPError:
                pass
        except urllib.error.URLError:
            pass
        TrafficLightStatus.set_status(open)
        if open:
            print("OPEN")
        else:
            print("CLOSED")
