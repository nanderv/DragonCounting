from django import template
from django.utils.http import urlencode

register = template.Library()


@register.inclusion_tag('reserve_day.html')
def reserve_view(timeslots, day):
    if day > 0:
        print(day)
    my_timeslots = []
    for timeslot in timeslots:
        if timeslot.is_on_days_future(day):
            my_timeslots.append(timeslot)
    return {'tss': my_timeslots, 'day': day}


@register.inclusion_tag('reservation_tbl.html')
def get_reservations(timeslot, day):
    res = timeslot.get_reservations_future(day)
    if len(res) > 0:
        return {'reservations': res, 'options': timeslot.get_options()}
    else:
        return {"nope": True}


@register.simple_tag
def day_nr(day):
    if day == 0:
        return "Today"
    if day == 1:
        return "Tomorrow"
    if day == 2:
        return "Overmorrow"
    return day


@register.inclusion_tag('forced_open_ts.html')
def forced_open(timeslot, day):
    z = 1
    if timeslot.is_forced_open(day):
        z =0
    return {'timeslot': timeslot, 'day': day, 'should_open': z }
