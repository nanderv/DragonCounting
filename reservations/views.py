from datetime import date

from django.shortcuts import render

# Create your views here.
from reservations.forms import EditForm
from reservations.models import Reservation
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

    available_afternoon = len(Reservation.objects.filter(timeslot='afternoon'))
    available_evening = len(Reservation.objects.filter(timeslot='evening'))
    return render(request, 'reserve.html',
                  {'form': form, 'instance': instance, 'maximum': settings.MAX_RESERVE, 'available_afternoon': available_afternoon, 'available_evening': available_evening})
