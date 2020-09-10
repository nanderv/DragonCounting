from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from crowd_counting.models import CrowdStatus
from traffic_light.models import TrafficLightStatus
from django.conf import settings


def view(request):
    print(request.POST)
    if request.POST and not request.user.is_anonymous:
        crowd = request.POST.get('crowd')
        CrowdStatus.set_status(crowd)
    crowd_status = CrowdStatus.objects.filter(to_datetime=None)
    crowd = 0
    if len(crowd_status) == 1:
        crowd = crowd_status[0].crowd
    light = TrafficLightStatus.objects.filter(to_datetime=None)
    open = False
    if len(light) == 1:
        open = light[0].open
    return render(request, 'crowd_view.html',
                  {'crowd': crowd, 'open': open, 'max': settings.MAX_CROWD, 'full': crowd >= settings.MAX_CROWD})


def crowd_api(request):
    crowd_status = CrowdStatus.objects.filter(to_datetime=None)
    crowd = 0
    if len(crowd_status) == 1:
        crowd = crowd_status[0].crowd
    light = TrafficLightStatus.objects.filter(to_datetime=None)
    open = False
    if len(light) == 1:
        open = light[0].open
    return HttpResponse(str(crowd)+","+str(settings.MAX_CROWD)+","+ str(open))
