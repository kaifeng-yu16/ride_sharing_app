from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ride
from django.db.models import Q
from .forms import OwnerRideForm, DriverJoinForm
from django.utils import timezone
# Create your views here.

@login_required
def owner_view(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    sharer_num = len(ride.sharer_set.all())
    return render(request, 'ride/owner_view.html', locals())

@login_required
def owner_edit(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    if ride.status != 'open':
        return HttpResponse('This ride can not be edit!')
    if len(ride.sharer_set.all()) == 0:
        not_shared = True
    time = timezone.localtime(ride.arrival_time).strftime('%Y-%m-%dT%H:%M')
    if request.method == "GET":
        owner_form = OwnerRideForm(instance=ride)
        return render(request, 'ride/owner_update.html', locals())
    else:
        owner_form = OwnerRideForm(request.POST, instance=ride)
        if 'cancel' in request.POST:
            ride.status = 'cancel'
            ride.save()
            messages.add_message(request, messages.INFO, 'Cancel a ride!')
            return HttpResponseRedirect(reverse('ride:home'))
        if owner_form.is_valid():
            owner_form.save()
            num_old = ride.num_owners
            num_new =  int(request.POST['num_owner'])
            ride.num_passengers += (num_new - num_old)
            ride.num_owners = request.POST['num_owner']
            ride.arrival_time = request.POST['arrival_time']
            ride.save()
            messages.add_message(request, messages.INFO, 'Successfully update owner ride!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong when editing owner ride. Please try again!')
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
def sharer_join(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    if ride.status == 'cancel':
        return HttpResponse('This ride was canceled by owner!')
    elif ride.status == 'open':
        if request.method == "POST":
            driver_join_form = DriverJoinForm(request.POST, instance=ride)
            if driver_join_form.is_valid():
                driver_join_form.save()
                ride.status = 'confirm'
                ride.driver = request.user
                ride.vehicle_type = request.user.vehicle_type
                ride.save()
                messages.add_message(request, messages.INFO, 'Join the Ride Successfully!')
                return HttpResponseRedirect(reverse('ride:home'))
            else:
                messages.add_message(request, messages.INFO, 'Something went wrong when joining the ride. Please try again!')
                return HttpResponseRedirect(reverse('ride:home'))
        else:
            driver_join_form = DriverJoinForm(instance=ride)
            return render(request, 'ride/driver_join.html', locals())
    else:
        return HttpResponse('This ride has been joined by other driver!')

@login_required
def owner_update(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Exception as e:
        return HttpResponse('The ride is not existed!')

    if request.method == "GET":

        return render(request, 'ride/owner_update.html', locals())
    elif request.method == "POST":
        pass

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
