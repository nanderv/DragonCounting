from django.forms import ModelForm, Select

from reservations.models import Reservation, Register, Timeslot

from django.forms import Select


class EditForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super (EditForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['timeslot'].queryset = Timeslot.objects.only_current()
    class Meta:
        model = Reservation
        fields = ['name',
                  'timeslot',

                  ]
        labels = {'name': 'Name',
                  'timeslot': 'Timeslot'
                  }
        widgets={'timeslot': Select}


class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['name',
                  'email'


                  ]
        labels = {'name': 'Name',
                  'email': 'Email',
                  }
