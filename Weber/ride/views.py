from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ride, Sharer
from django.db.models import Q
from .forms import OwnerRideForm
from django.utils import timezone
from django.core.mail import send_mail
# Create your views here.

@login_required
def owner_view(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    if ride.owner != request.user:
        return HttpResponse('This is not your ride. Can not view.')
    sharer_num = len(ride.sharer_set.all())
    return render(request, 'ride/owner_view.html', locals())

@login_required
def owner_edit(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    if ride.owner != request.user:
        return HttpResponse('This is not your ride. Can not edit.')
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
            num_new = int(request.POST['num_owner'])
            ride.num_passengers += (num_new - num_old)
            ride.num_owners = request.POST['num_owner']
            if len(ride.sharer_set.all()) != 0:
                ride.allow_share=True
            ride.arrival_time = request.POST['arrival_time']
            ride.save()
            messages.add_message(request, messages.INFO, 'Successfully update owner ride!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong when editing owner ride. Please try again!')
            return HttpResponseRedirect(reverse('ride:home'))

@login_required
def sharer_view(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    sharer_num = len(ride.sharer_set.all())
    try:
        sharer = ride.sharer_set.get(sharer=request.user)
    except Model.DoesNotExist:
        return HttpResponse('This is not your ride. Can not view.')
    return render(request, 'ride/sharer_view.html', locals())

@login_required
def sharer_edit(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    try:
        sharer = ride.sharer_set.get(sharer=request.user)
    except Model.DoesNotExist:
        return HttpResponse('This is not your ride. Can not edit.')
    if ride.status != 'open':
        return HttpResponse('This ride can not be edit!')
    if request.method == "GET":
        return render(request, 'ride/sharer_update.html', locals())
    else:
        if 'cancel' in request.POST:
            ride.num_passengers -= sharer.num_of_sharers
            ride.save()
            ride.sharer_set.filter(sharer=request.user).delete()
            messages.add_message(request, messages.INFO, 'Cancel a ride as sharer!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            num_old = sharer.num_of_sharers
            num_new = int(request.POST['num_sharer'])
            ride.num_passengers += (num_new - num_old)
            ride.save()
            sharer.num_of_sharers = request.POST['num_sharer']
            sharer.save()
            messages.add_message(request, messages.INFO, 'Successfully update sharer ride!')
            return HttpResponseRedirect(reverse('ride:home'))

@login_required
def driver_view(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    try:
        ride.driver
        request.user.driver
    except ObjectDoesNotExist:
        return HttpResponse('This ride does not have a driver or you are not a driver. Can not view.')
    else:
        if ride.driver != request.user.driver:
            return HttpResponse('This is not your ride. Can not view.')
    sharer_num = len(ride.sharer_set.all())
    return render(request, 'ride/driver_view.html', locals())

@login_required
def driver_edit(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    try:
        ride.driver
        request.user.driver
    except ObjectDoesNotExist:
        return HttpResponse('This ride does not have a driver or you are not a driver. Can not edit.')
    else:
        if ride.driver != request.user.driver:
            return HttpResponse('This is not your ride. Can not edit.')
    if ride.status != 'confirm':
        return HttpResponse('This ride can not be edit!')
    ride.status = 'complete'
    ride.save()
    messages.add_message(request, messages.INFO, 'Successfully complete a ride as driver!')
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
            if not ride.allow_share or ride.status != 'open' or request.user in ride.sharer_set:
                return HttpResponse('Invalid Access!')
            num_of_sharers = request.POST['num_of_sharers']
            sharer = Sharer.objects.create(ride=ride, sharer=request.user, num_of_sharers=num_of_sharers)
            ride.num_passengers += int(num_of_sharers)
            ride.save()
            messages.add_message(request, messages.INFO, 'Join the Ride Successfully!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            sharer_num = len(ride.sharer_set.all())
            return render(request, 'ride/sharer_join.html', locals())
    else:
        return HttpResponse('This ride has been confirmed by driver! Find another open ride to join!')

@login_required
def driver_join(request, ride_id):
    if not hasattr(request.user, 'driver'):
        messages.add_message(request, messages.INFO, 'You are not a driver!')
        return HttpResponseRedirect(reverse('ride:home'))
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return HttpResponse('This ride is not existed!')
    if ride.status == 'cancel':
        return HttpResponse('This ride was canceled by owner!')
    elif ride.status == 'open':
        if request.method == "POST":
            if ride.status != 'open' or ride.num_passengers > request.user.driver.max_volume or \
                    ride.special_request != request.user.driver.special_info or \
                    (ride.vehicle_type != '-' and ride.vehicle_type != request.user.driver.vehicle_type):
                return HttpResponse('Invalid Access!')
            ride.status = 'confirm'
            ride.driver = request.user.driver
            ride.save()
            send_mail(
                'Driver has confirmed your ride!',
                'Your ride has been confirmed by driver.',
                'weber-easy-ride@outlook.com',
                [ride.owner.email],
            )
            sharer_emails = list(s.sharer.email for s in request.user.sharer_set.all())
            if len(sharer_emails) != 0:
                send_mail(
                    'Driver has confirmed your ride!',
                    'Your ride has been confirmed by driver.',
                    'weber-easy-ride@outlook.com',
                    sharer_emails,
                )
            messages.add_message(request, messages.INFO, 'Join the Ride Successfully!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            return render(request, 'ride/driver_join.html', locals())
    else:
        return HttpResponse('This ride has been joined by other driver!')

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
        ride = Ride.objects.create(owner=owner, num_owners=num_owners, num_passengers=num_passengers, \
                                   destination=destination, status=status, arrival_time=arrival_time, \
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
    if not hasattr(request.user, 'driver'):
        messages.add_message(request, messages.INFO, 'You are not a driver!')
        return HttpResponseRedirect(reverse('ride:home'))
    if request.method == "POST":
        sharer_ride_id = list(s.ride.id for s in request.user.sharer_set.all())
        search_results = Ride.objects.filter(status='open', num_passengers__lte=request.user.driver.max_volume) \
            .filter(Q(special_request=request.user.driver.special_info) | Q(special_request='')) \
            .filter(Q(vehicle_type='-') | Q(vehicle_type=request.user.driver.vehicle_type)).exclude(owner=request.user) \
            .exclude(id__in=sharer_ride_id)
        return render(request, 'ride/search_as_driver.html', {'has_result': True, 'search_results': search_results})
    else:
        return render(request, 'ride/search_as_driver.html')

@login_required
def home(request):
    owner_ride=request.user.ride_set.all()
    sharer=request.user.sharer_set.all()
    sharer_ride=request.user.ride_set.none()
    for s in sharer:
        sharer_ride |= Ride.objects.filter(pk=s.ride.pk)
    print(type(sharer_ride))
    if hasattr(request.user, "driver"):
        driver_ride=request.user.driver.ride_set.all()
    else:
        driver_ride=[]
    return render(request, 'ride/home.html', {'owner': owner_ride, 'sharer': sharer_ride, 'driver': driver_ride});
