from datetime import date

from django.shortcuts import render, redirect

# Create your views here.
from reservations.forms import EditForm
from reservations.models import Reservation, Timeslot
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
    return render(request, 'reserve.html', {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'timeslots':timeslots})


def view2(request):
    Reservation.wipe()
    instance = None
    form = EditForm()

    timeslots = Timeslot.objects.all()
    return render(request, 'reserve.html', {'form': form, 'instance': True, 'maximum': settings.MAX_RESERVE, 'timeslots':timeslots})


def delete(request, id):
    reservation = Reservation.objects.get(pk=id)
    if not request.GET.get('confirm'):
        return render(request, 'are-you-sure.html', {'what': "delete reservation with name " + reservation.name +" for " + reservation.timeslot.name})
    reservation.delete()
    return redirect('reserve')