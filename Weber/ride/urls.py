from django.urls import path
from . import views

app_name = 'ride'
urlpatterns = [
    path('home/', views.home, name='home'),
]
