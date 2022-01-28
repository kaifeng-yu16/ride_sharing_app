from django.shortcuts import render

# Create your views here.
def create_ride(request):
    if request.method == "GET":
        return render(request, 'ride/create_ride.html')
'''    elif request.method == "POST":
        return render(request, )
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
            return HttpResponseRedirect(reverse('user:login'))'''