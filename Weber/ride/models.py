from django.db import models

# Create your models here.
class Ride(models.Model):
     status = models.CharField(max_length=10)
