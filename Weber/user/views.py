from django.shortcuts import render

# Create your views here.

def welcome(request):
    return render(request, 'user/welcome.html')

def logout(request):
    return render(request, 'user/logout.html')

def change_info(request):
    return render(request, 'user/change_info.html')
