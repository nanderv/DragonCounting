from datetime import date

from django.shortcuts import render, redirect
from django.db import transaction

# Create your views here.
from reservations.forms import EditForm
from reservations.models import Reservation, Timeslot, TimeslotOption, TimeslotOptionValue
from django.conf import settings


def view(request):
    Reservation.wipe()
    instance = None
    form = EditForm()

    if request.POST:
        form = EditForm(request.POST)
        instance = form.save(commit=False)
        instance.date = date.today()

        return redirect('reserve.options', instance.timeslot.id, instance.name)

    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html', {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'timeslots': timeslots})


def view2(request):
    Reservation.wipe()
    instance = None
    form = EditForm()

    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html', {'form': form, 'instance': True, 'maximum': settings.MAX_RESERVE, 'timeslots': timeslots})

@transaction.atomic
def options(request, id, name):
    timeslot = Timeslot.objects.get(pk=id)
    options = TimeslotOption.objects.filter(timeslot=timeslot)
    if len(options) == 0 or request.POST:
        reservation = Reservation.objects.create(name=name, timeslot=timeslot, date=date.today())
        any_on = False
        for option in options:
            any_on = any_on or  request.POST.get(str(option.pk), False) == "on"
            TimeslotOptionValue.objects.create(timeslot_option=option, value=request.POST.get(str(option.pk), False) == "on", reservation=reservation)
        if not any_on:
            reservation.delete()
            return render(request, 'options.html', {'instance': True, 'timeslot': timeslot, 'options': options,'warning':'You can only visit Bellettrie for one of the reasons below.'})
        return redirect('reserved')
    return render(request, 'options.html', {'instance': True, 'timeslot': timeslot, 'options': options})


def delete(request, id):
    reservation = Reservation.objects.get(pk=id)
    if not request.GET.get('confirm'):
        return render(request, 'are-you-sure.html', {'what': "delete reservation with name " + reservation.name + " for " + reservation.timeslot.name})
    reservation.delete()
    return redirect('reserve')
