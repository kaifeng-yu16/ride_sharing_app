from django.db import models

from user.models import Driver
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
VEHICLE_TYPE = {
    ("-", "-"),
    ("Comfort", "Comfort"),
    ("Luxury", "Luxury"),
    ("Sports", "Sports"),
    ("SUV", "SUV"),
}

RIDE_STATUS = {
    ("open", "open"),
    ("confirm", "confirm"),
    ("complete", "complete"),
}
class Ride(models.Model):
     # from owner side
     owner = models.ForeignKey(User, on_delete=models.CASCADE)
     num_owners = models.PositiveIntegerField(default=1)
     num_passengers = models.PositiveIntegerField()
     destination = models.CharField(max_length=100)
     status = models.CharField(default='open', choices=RIDE_STATUS, max_length=10)
     arrival_time = models.DateTimeField()
     allow_share = models.BooleanField(default=False)
     vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE)
     special_request = models.TextField(blank=True, default='')

     # from driver side
     driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)

     def __str__(self):
          return '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.owner.username, self.num_owners, self.destination, self.status,\
                                            self.arrival_time, self.vehicle_type, self.allow_share, self.special_request,\
                                            self.driver)

class Sharer(models.Model):
     ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
     sharer = models.ForeignKey(User, on_delete=models.CASCADE)
     num_of_sharers = models.PositiveIntegerField(default=1)
