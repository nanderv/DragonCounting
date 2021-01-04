from datetime import date, timedelta

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
        if not instance.date:
            instance.date = date.today()

        return redirect('reserve.options', instance.timeslot.id, instance.name, instance.date)
    data_dict = dict()
    today = date.today()
    data_dict[today.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(today, True)
    tomorrow = date.today()+ timedelta(days=1)
    data_dict[tomorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(tomorrow)
    overmorrow = date.today() + timedelta(days=2)
    data_dict[overmorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(overmorrow)
    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html', {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'timeslots': timeslots, 'tds':data_dict})


def view2(request):
    Reservation.wipe()
    instance = None
    form = EditForm()

    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html', {'form': form, 'instance': True, 'maximum': settings.MAX_RESERVE, 'timeslots': timeslots})

@transaction.atomic
def options(request, id, name, date):
    timeslot = Timeslot.objects.get(pk=id)
    options = TimeslotOption.objects.filter(timeslot=timeslot)
    if len(options) == 0 or request.POST:
        reservation = Reservation.objects.create(name=name, timeslot=timeslot, date=date)
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
