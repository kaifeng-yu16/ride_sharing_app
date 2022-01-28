from .models import Driver
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
        lisence = request.POST['Lisence']
        vehicle_type = request.POST['Type']
        volume = request.POST['Volume']
        info = request.POST['Info']
        d = Driver(user=request.user, vehicle_type=vehicle_type, lisence=lisence, max_volume=volume, special_info=info)
        d.save()
        messages.add_message(request, messages.INFO, 'Create Driver Profile Successfully!')
        return HttpResponseRedirect(reverse('ride:home'))


@login_required
def change_info(request):
    return render(request, 'user/change_info.html')
