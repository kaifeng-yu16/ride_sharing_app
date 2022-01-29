from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Ride


@login_required
def create_ride(request):
    if request.method == "POST":
        owner = request.user
        num_owners = request.POST['num'] 
        num_passengers = num_owners
        destination = request.POST['destination']
        status = 'open'
        arrival_time = request.POST['arrival_time']
        if 'share' in request.POST:
            allow_share = True
        else:
            allow_share = False
        vehicle_type = request.POST['vehicle']
        special_request = request.POST['request']
        ride = Ride.objects.create(owner=owner, num_owners=num_owners, num_passengers=num_passengers,\
                                   destination=destination, status=status, arrival_time=arrival_time,\
                                   vehicle_type=vehicle_type, allow_share=allow_share, special_request=special_request)
        messages.add_message(request, messages.INFO, 'Ride Create Successfully!')
        return HttpResponseRedirect(reverse('ride:home'))
    else:
        return render(request, 'ride/create_ride.html')


def search_ride(request):
    if request.method == "POST":
        # search_results = Ride.objects.all()
        destination = request.POST['destination']
        early_time = request.POST['early_time']
        late_time = request.POST['late_time']
        num_passenger = request.POST['num_passenger']
        search_results = Ride.objects.filter(destination=destination, status='open',
                                             time__range=(early_time, late_time),
                                             share=True)
        return render(request, 'ride/search_ride_as_sharer.html', {'search_results': search_results})
    else:
        return render(request, 'ride/search_ride_as_sharer.html')

def home(request):
    return render(request, 'ride/home.html');
