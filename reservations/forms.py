from datetime import datetime, timedelta

from django.forms import ModelForm, Select, forms, ChoiceField

from reservations.models import Reservation, Timeslot


CATEGORIES = (
    ('COM', 'Combat'),
    ('CRA', 'Crafting'),
    ('WAR', 'Warfare'),
)
def today_options():
    return (
        (
        datetime.now().date(), "Today: "+ str(datetime.now().date().isoformat())
        ),
        ( (datetime.now()+timedelta(days=1)).date(), "Tomorrow: "+ str((datetime.now()+timedelta(days=1)).date().isoformat())),
        ((datetime.now() + timedelta(days=2)).date(), "Overmorrow: " + str((datetime.now() + timedelta(days=2)).date().isoformat())),
    )
class EditForm(ModelForm):
    date = ChoiceField(choices=today_options())
    def __init__(self,*args,**kwargs):
        super (EditForm,self ).__init__(*args,**kwargs) # populates the post
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
        widgets={'timeslot': Select}


