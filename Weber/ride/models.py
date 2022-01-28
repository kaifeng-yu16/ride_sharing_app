from django.db import models

# Create your models here.
class Ride(models.Model):
     # from owner side
     owner = models.CharField(max_length=100)
     num_owners = models.PositiveIntegerField(default=1)
     destination = models.CharField(max_length=100)
     status = models.CharField(default='open', max_length=10)
     arrival_time = models.DateTimeField()
     vehicle_type = models.CharField(max_length=10, blank=True)
     share = models.BooleanField(default=False)
     special_request = models.CharField(max_length=200, blank=True)

     # from driver side
     driver = models.CharField(max_length=100)
     license = models.CharField(max_length=20)
     vehicle_volume = models.PositiveIntegerField(default=0)
     special_vehicle_info = models.CharField(max_length=200, blank=True)

     # from sharer side
     #sharers = models.ForeignKey('Sharer', blank=True)

     def __str__(self):
          return '%s %s %s %s %s %s %s %s %s %s %s %s'%(self.owner, self.num_owners, self.destination, self.status,
                                            self.arrival_time, self.vehicle_type, self.share, self.special_request,
                                            self.driver, self.license, self.vehicle_volume, self.special_vehicle_info)

class Sharer(models.Model):
     num_of_sharers = models.PositiveIntegerField(default=1)