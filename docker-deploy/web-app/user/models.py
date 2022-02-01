from django.db import models
from django.contrib.auth.models import User

# Create your models here.
VEHICLE_TYPE = {
    ("Comfort", "Comfort"),
    ("Luxury", "Luxury"),
    ("Sports", "Sports"),
    ("SUV", "SUV"),
}

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    vehicle_type =  models.CharField(max_length=10, choices=VEHICLE_TYPE)
    license =  models.CharField(max_length=200)
    max_volume = models.PositiveIntegerField()
    special_info = models.TextField(blank=True, default='')
    def __str__(self):
        return self.user.username
