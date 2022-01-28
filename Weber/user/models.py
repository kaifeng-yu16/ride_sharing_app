from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    vehicle_type =  models.CharField(max_length=200)
    lisence =  models.CharField(max_length=200)
    max_volume = models.PositiveIntegerField(default=4)
    special_info = models.TextField(blank=True, default='')
    def __str__(self):
        return self.user.username
