from django.db import models
from user.models import Driver
from django.contrib.auth.models import User

# Create your models here.
RIDE_STATUS = {
    ("open", "open"),
    ("confirm", "confirm"),
    ("complete", "complete"),
}
class Ride(models.Model):
     # from owner side
     owner = models.ForeignKey(User, on_delete=models.CASCADE)
     num_owners = models.PositiveIntegerField(default=1)
     destination = models.CharField(max_length=100)
     status = models.CharField(default='open', choices=RIDE_STATUS, max_length=10)
     arrival_time = models.DateTimeField()
     allow_share = models.BooleanField(default=False)
     vehicle_type = models.CharField(max_length=10, blank=True)
     special_request = models.CharField(max_length=200, blank=True)

     # from driver side
     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

     def __str__(self):
          return '%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.owner, self.num_owners, self.destination, self.status,
                                            self.arrival_time, self.vehicle_type, self.share, self.special_request,
                                            self.driver, self.license, self.vehicle_volume, self.special_vehicle_info)

class Sharer(models.Model):
     sharer = models.ForeignKey(User, on_delete=models.CASCADE)
     num_of_sharers = models.PositiveIntegerField(default=1)
