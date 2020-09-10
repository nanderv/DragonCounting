from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from traffic_light.models import TrafficLightStatus


def view_light(request):
    ts = TrafficLightStatus.objects.filter(to_datetime=None)
    if len(ts) ==1 and ts[0].open:
        return HttpResponse("true")
    else:
        return HttpResponse("false")