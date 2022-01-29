from django.db import models
from django.utils import timezone

# Create your models here.
class Ride(models.Model):
     # from owner side
     owner = models.CharField(max_length=100)
     num_owners = models.PositiveIntegerField(default=1)
     destination = models.CharField(max_length=100)
     status = models.CharField(default='open', max_length=10)
     arrival_date = models.DateField(default=timezone.now())
     arrival_time = models.TimeField(default=timezone.now())
     vehicle_type = models.CharField(max_length=10, blank=True)
     allow_share = models.BooleanField(default=False)
     special_request = models.CharField(max_length=200, blank=True)

     # from driver side
     driver = models.CharField(max_length=100)

     # from sharer side
     # sharers = models.ForeignKey('Sharer', on_delete=models.CASCADE)
     #sharers = models.

     def __str__(self):
          return '%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.owner, self.num_owners, self.destination, self.status,
                                            self.arrival_time, self.vehicle_type, self.share, self.special_request,
                                            self.driver, self.license, self.vehicle_volume, self.special_vehicle_info)

class Sharer(models.Model):
     num_of_sharers = models.PositiveIntegerField(default=1)