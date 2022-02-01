from .models import Driver
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, DriverProfileForm

# Create your views here.

def welcome(request):
    return render(request, 'user/welcome.html')

def logout(request):
    return render(request, 'user/logout.html')

def create_account(request):
    if request.method == "GET":
        return render(request, 'user/create_account.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'user/create_account.html', {'existed_user': True})
        else: 
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.add_message(request, messages.INFO, 'Create Successfully! Please log in.')
            return HttpResponseRedirect(reverse('user:login'))

@login_required
def add_driver(request):
    if request.method == "GET":
        return render(request, 'user/add_driver.html')
    else:
        if hasattr(request.user, "driver"):
            return HttpResponse('You are already a driver!')
        first_name = request.POST['first']
        last_name = request.POST['last']
        license = request.POST['License']
        vehicle_type = request.POST['Type']
        volume = request.POST['Volume']
        info = request.POST['Info']
        d = Driver(user=request.user, first_name=first_name, last_name=last_name, vehicle_type=vehicle_type, license=license, max_volume=volume, special_info=info)
        d.save()
        messages.add_message(request, messages.INFO, 'Create Driver Profile Successfully!')
        return HttpResponseRedirect(reverse('ride:home'))


@login_required
def change_info(request):
    if request.method == "GET":
        user_form = UserProfileForm(instance=request.user)
        driver_form = ''
        if hasattr(request.user, 'driver'): 
            driver_form = DriverProfileForm(instance=request.user.driver)
        return render(request, 'user/change_info.html', {'user_form': user_form, 'driver_form': driver_form})
    else:
        user_form = UserProfileForm(request.POST, instance=request.user)
        if hasattr(request.user, 'driver'):
            driver_form = DriverProfileForm(request.POST, instance=request.user.driver)
        if 'driver_del' in request.POST:
            if ('confirm', ) in request.user.driver.ride_set.all().values_list('status'):
                return HttpResponse('Please complete all of your rides as a driver before deleting your driver identity!')
            request.user.driver.delete()
            messages.add_message(request, messages.INFO, 'Not a driver anymore!')
            return HttpResponseRedirect(reverse('ride:home'))
        if user_form.is_valid() and (not hasattr(request.user, 'driver')\
                or driver_form.is_valid()):
            user_form.save()
            if hasattr(request.user, 'driver'):
                driver_form.save()
                request.user.driver.max_volume = request.POST['Volume']
                request.user.driver.save()
            messages.add_message(request, messages.INFO, 'Edit User Profile Successfully!')
            return HttpResponseRedirect(reverse('ride:home'))
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong when editing user profile. Please try again!')
            return HttpResponseRedirect(reverse('ride:home'))


@login_required
def show_info(request):
    return render(request, 'user/show_info.html')
