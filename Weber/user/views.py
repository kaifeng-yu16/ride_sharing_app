from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect

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


def change_info(request):
    return render(request, 'user/change_info.html')
