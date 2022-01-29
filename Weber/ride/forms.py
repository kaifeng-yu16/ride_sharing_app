from django.forms import ModelForm
from .models import Ride, Sharer

class OwnerRideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['num_owners', 'destination', 'status', 'arrival_time',
                  'allow_share', 'vehicle_type', 'special_request']

class SharerRideForm(ModelForm):
    class Meta:
        model = Sharer
        fields = ['num_of_sharers']
