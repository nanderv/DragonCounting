from datetime import date

from django.shortcuts import render

# Create your views here.
from reservations.forms import EditForm, RegisterForm
from reservations.models import Reservation, Register, Timeslot
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
    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html',
                  {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'timeslots':timeslots})


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
