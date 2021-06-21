from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from crowd_counting.models import CrowdStatus
from reservations.models import Timeslot
from traffic_light.models import TrafficLightStatus
from django.conf import settings


def view(request):
    print(request.POST)
    if request.POST and not request.user.is_anonymous:
        crowd = request.POST.get('crowd')
        CrowdStatus.set_status(crowd)
        return redirect('traffic_light.view')
    crowd_status = CrowdStatus.objects.filter(to_datetime=None)
    crowd = 0
    if len(crowd_status) == 1:
        crowd = crowd_status[0].crowd
    light = TrafficLightStatus.objects.filter(to_datetime=None)
    open = False
    if len(light) == 1:
        open = light[0].open
    reserved = 0
    for t in Timeslot.objects.all():
        reserved += (t.get_timeslot_number_people_now())
    return render(request, 'crowd_view.html',
                  {'crowd': crowd, 'open': open, 'max': settings.MAX_CROWD, 'full': crowd >= settings.MAX_CROWD,
                   'name': request.session.get("name", ""), 'reserved_count': reserved})


def crowd_api(request):
    crowd_status = CrowdStatus.objects.filter(to_datetime=None)
    crowd = 0
    if len(crowd_status) == 1:
        crowd = crowd_status[0].crowd
    light = TrafficLightStatus.objects.filter(to_datetime=None)
    open = False
    if len(light) == 1:
        open = light[0].open
    count = 0
    for t in Timeslot.objects.all():
        count += (t.get_timeslot_number_people_now())
    return HttpResponse(
        str(crowd) + "," + str(settings.MAX_CROWD) + "," + str(open) + "," + str(settings.MAX_CROWD - count))


def diff(request, delta):
    crowd_status = CrowdStatus.objects.filter(to_datetime=None)
    crowd = 0
    if len(crowd_status) == 1:
        crowd = crowd_status[0].crowd
    crowd += int(delta)
    CrowdStatus.set_status(crowd)

    return redirect('traffic_light.view')
