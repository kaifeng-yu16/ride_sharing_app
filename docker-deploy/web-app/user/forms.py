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
        fields = ['first_name', 'last_name', 'vehicle_type', 'license', 'special_info']
