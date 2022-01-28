from django.urls import path

from Weber.ride import views

urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride'),
]