from datetime import date, timedelta, datetime, time

from django.forms import ModelForm, Select, forms, ChoiceField

from reservations.models import Reservation, Timeslot

HOURS = 15


def today_options():
    today = datetime.now().date()
    res = ()
    if len(Timeslot.objects.available_on_day(today, True)) > 0:
        res = res + ((
                         datetime.now().date(), "Today: " + str(datetime.now().date().isoformat()))
        ,)

    z = Timeslot.objects.available_on_day(
        (datetime.now() + timedelta(days=1)).date(),
        datetime.now().time() > time(HOURS, 0))
    if len(z) > 0:
        res = res + ((((datetime.now() + timedelta(days=1)).date(),
                       "Tomorrow: " + str((datetime.now() + timedelta(days=1)).date().isoformat()))),)
    if len(Timeslot.objects.available_on_day(
            (datetime.now() + timedelta(days=2)).date(), False)) > 0:
        res = res + ((((datetime.now() + timedelta(days=2)).date(),
                       "Overmorrow: " + str(
                           (datetime.now() + timedelta(days=2)).date().isoformat()))),)
    return res


class EditForm(ModelForm):
    date = ChoiceField(choices=today_options())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('date').choices = today_options()
        self.fields['timeslot'].queryset = Timeslot.objects.all()

    class Meta:
        model = Reservation
        fields = ['name',
                  'date',
                  'timeslot',
                  ]
        labels = {'name': 'Name',
                  'timeslot': 'Timeslot'
                  }
        widgets = {'timeslot': Select}
