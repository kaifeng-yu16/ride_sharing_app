from django.forms import ModelForm
from .models import Driver
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class DriverProfileForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['vehicle_type', 'license', 'max_volume', 'special_info']
