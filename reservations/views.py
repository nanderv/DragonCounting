from datetime import date

from django.shortcuts import render

# Create your views here.
from reservations.forms import EditForm, RegisterForm
from reservations.models import Reservation, Register
from django.conf import settings


def view(request):
    Reservation.wipe()
    instance = None
    form = EditForm()

    if request.POST:
        form = EditForm(request.POST)
        instance = form.save(commit=False)
        instance.date = date.today()
        instance.save()
    afternoon_res = Reservation.objects.filter(timeslot='afternoon', date=date.today())
    available_afternoon = len(afternoon_res)
    evening_res = Reservation.objects.filter(timeslot='evening', date=date.today())
    available_evening = len(evening_res)
    return render(request, 'reserve.html',
                  {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'available_afternoon': available_afternoon, 'available_evening': available_evening,
                   'afternoon_res': afternoon_res, 'evening_res': evening_res})


def register(request):
    Register.wipe()
    instance = None
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        instance = form.save(commit=False)
        instance.date = date.today()
        instance.save()
    return render(request, 'register.html',
                  {'form': form, 'instance': instance})
