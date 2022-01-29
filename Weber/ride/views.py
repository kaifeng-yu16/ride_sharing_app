from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ride
from django.db.models import Q
# Create your views here.

@login_required
def owner_view(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def owner_edit(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def sharer_view(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def sharer_edit(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def driver_view(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def driver_edit(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def sharer_join(request):
    return HttpResponseRedirect(reverse('ride:home'))

@login_required
def driver_join(request):
    return HttpResponseRedirect(reverse('ride:home'))

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

@login_required
def search_as_sharer(request):
    if request.method == "POST":
        destination = request.POST['destination']
        early_time = request.POST['early_time']
        late_time = request.POST['late_time']
        search_results = Ride.objects.filter(destination=destination, status='open',
                                             arrival_time__range=(early_time, late_time),
                                             allow_share=True).exclude(owner=request.user)
        return render(request, 'ride/search_as_sharer.html', {'has_result': True, 'search_results': search_results})
    else:
        return render(request, 'ride/search_as_sharer.html')

@login_required
def search_as_driver(request):
    if request.method == "POST":
        if not hasattr(request.user, 'driver'):
            messages.add_message(request, messages.INFO, 'You are not a driver!')
            return HttpResponseRedirect(reverse('ride:home'))
        sharer_ride_id = list(s.ride.id for s in request.user.sharer_set.all())
        search_results = Ride.objects.filter(status='open', num_passengers__lte=request.user.driver.max_volume)\
            .filter(Q(special_request=request.user.driver.special_info)|Q(special_request=''))\
            .filter(Q(vehicle_type='-')|Q(vehicle_type=request.user.driver.vehicle_type)).exclude(owner=request.user)\
            .exclude(id__in=sharer_ride_id)
        return render(request, 'ride/search_as_driver.html', {'has_result':True, 'search_results': search_results})
    else:
        return render(request, 'ride/search_as_driver.html')

@login_required
def home(request):
    owner_ride=request.user.ride_set.all()
    sharer=request.user.sharer_set.all()
    sharer_ride=[s.ride for s in sharer]
    if hasattr(request.user, "driver"):
        driver_ride=request.user.driver.ride_set.all()
    else:
        driver_ride=[]
    return render(request, 'ride/home.html', {'owner': owner_ride, 'sharer': sharer_ride, 'driver': driver_ride});
