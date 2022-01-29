from django.shortcuts import render
from django.views.generic import ListView
from django.db import models

# Create your views here.
from .models import Ride


def create_ride(request):
    if request.method == "POST":
        destination = request.POST['destination']
        arrival_date = request.POST['arrival_date']
        arrival_time = request.POST['arrival_time']
        num_passengers = request.POST['num_passengers']
        vehicle_type = request.POST['vehicle_type']
        allow_share = request.POST['allow_share']
        special_request = request.POST['special_request']
        ride = Ride.objects.create(destination=destination, arrival_date=arrival_date, arrival_time=arrival_time, num_passengers=num_passengers,
                                   vehicle_type=vehicle_type, allow_share=allow_share, special_request=special_request)
        return render(request, 'ride/create_ride_success.html')
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
