from datetime import date, timedelta, datetime, time

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction

# Create your views here.
from reservations.forms import EditForm
from reservations.models import Reservation, Timeslot, TimeslotOption, TimeslotOptionValue, name_str_to_name, name_str_to_id, \
    ForceOpen
from django.conf import settings

HOURS = 15


def get_my_res(name):
    ress = Reservation.objects.all()
    my_list = []
    for res in ress:
        if res.get_id() == name and res.get_id() != "":
            my_list.append(res)
    return my_list


def view(request):
    my_res = get_my_res(request.session.get("my_id", ""))
    Reservation.wipe()
    instance = None
    form = EditForm()
    form.data['name'] = request.session.get('name', None)
    if request.POST:
        form = EditForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.date:
                instance.date = date.today()
        if not request.session.get('name'):
            if "@@" in instance.name:
                return HttpResponse("Name contains illegal characters")
            request.session['name'] = instance.name
        return redirect('reserve.options', instance.timeslot.id, instance.date)
    data_dict = dict()
    today = date.today()
    data_dict[today.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(today, True)
    tomorrow = date.today() + timedelta(days=1)
    trd = False

    if datetime.now().time() > time(HOURS, 0):
        trd = True
        data_dict[tomorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(tomorrow, True)
    else:
        data_dict[tomorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(tomorrow)

    overmorrow = date.today() + timedelta(days=2)
    data_dict[overmorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(overmorrow)
    timeslots = Timeslot.objects.all()
    name = request.session.get("name")
    nm = name or ""
    id = None

    if "@@" in nm:
        nm = name.split("@@")[0]

        if len(name.split("@@")) > 1:
            id = name.split("@@")[1]
    return render(request, 'reserve.html', {'my_registrations': my_res, 'after_time': trd, 'form': form, 'instance': instance,
                                            'maximum': settings.MAX_RESERVE, 'timeslots': timeslots,
                                            'tds': data_dict, 'name': nm, 'p_id': id})


def view2(request):
    my_res = get_my_res(request.session.get("my_id", ""))
    Reservation.wipe()
    instance = None
    form = EditForm()
    data_dict = dict()
    today = date.today()
    data_dict[today.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(today, True)
    tomorrow = date.today() + timedelta(days=1)
    trd = False
    if datetime.now().time() > time(HOURS, 0):
        trd = True
        data_dict[tomorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(tomorrow, True)
    else:
        data_dict[tomorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(tomorrow)
    overmorrow = date.today() + timedelta(days=2)
    data_dict[overmorrow.strftime('%Y-%m-%d')] = Timeslot.objects.available_on_day(overmorrow)
    timeslots = Timeslot.objects.all()

    return render(request, 'reserve.html',
                  {'my_registrations': my_res, 'after_time': trd, 'form': form, 'instance': True,
                   'maximum': settings.MAX_RESERVE, 'timeslots': timeslots,
                   'tds': data_dict, 'name': request.session.get("name", "")})


@transaction.atomic
def options(request, id, date):
    timeslot = Timeslot.objects.get(pk=id)
    name = request.session['name']
    my_id = request.session.get("my_id", None)
    options = TimeslotOption.objects.filter(timeslot=timeslot)
    if len(options) == 0 or request.POST:
        reservation = Reservation.objects.create(name=name, timeslot=timeslot, date=date, my_id=my_id)
        any_on = False
        for option in options:
            any_on = any_on or request.POST.get(str(option.pk), False) == "on"
            TimeslotOptionValue.objects.create(timeslot_option=option, value=request.POST.get(str(option.pk), False) == "on",
                                               reservation=reservation)
        if not any_on and len(options) > 0:
            reservation.delete()
            return render(request, 'options.html', {'instance': True, 'timeslot': timeslot, 'options': options,
                                                    'warning': 'You need to select an option below. If none are available, then the activity is full.'})
        return redirect('reserved')
    return render(request, 'options.html',
                  {'instance': True, 'timeslot': timeslot, 'options': options, 'name': request.session.get("name", "")})


def delete(request, id):
    reservation = Reservation.objects.get(pk=id)

    if not (request.user.is_authenticated or (
            reservation.get_id() != "" and reservation.get_id() == name_str_to_id(request.session.get("name", "") or ""))):
        return HttpResponse("ERROR")

    if not request.GET.get('confirm'):
        return render(request, 'are-you-sure.html',
                      {'what': "delete reservation with name " + reservation.name + " for " + reservation.timeslot.name})
    reservation.delete()
    return redirect('reserve')


def arrive(request, id):
    reservation = Reservation.objects.get(pk=id)

    if not (request.user.is_authenticated or (
            reservation.get_id() != "" and reservation.get_id() == name_str_to_id(request.session.get("name", "") or ""))):
        return HttpResponse("ERROR")
    reservation.arrived = True
    reservation.save()
    return redirect('reserve')


def logout(request):
    request.session['name'] = None
    request.session['my_id'] = None
    return redirect('logout')


@permission_required('perms.reservations.change_reservation')
def force_timeslot_open(request, id, d, to_open):
    ts = Timeslot.objects.get(pk=id)
    date = datetime.today() + timedelta(days=d)
    ForceOpen.objects.filter(timeslot=ts, date=date).delete()
    if to_open:
        ForceOpen.objects.create(timeslot=ts, date=date)
    return redirect('reserve')
