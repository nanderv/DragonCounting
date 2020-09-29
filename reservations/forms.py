from django.forms import ModelForm

from reservations.models import Reservation


class EditForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name',
                  'timeslot',

                  ]
        labels = {'name': 'Name',
                  'timeslot': 'Timeslot'
                  }
