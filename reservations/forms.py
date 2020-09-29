from django.forms import ModelForm

from reservations.models import Reservation, Register


class EditForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name',
                  'timeslot',

                  ]
        labels = {'name': 'Name',
                  'timeslot': 'Timeslot'
                  }


class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['name',
                  'email'


                  ]
        labels = {'name': 'Name',
                  'email': 'Email',
                  }
