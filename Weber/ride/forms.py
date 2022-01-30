from django.forms import ModelForm
from .models import Ride, Sharer

class OwnerRideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'allow_share', 'vehicle_type', 'special_request']

'''class DriverJoinForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['driver', 'status']'''