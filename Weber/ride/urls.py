from django.urls import path

from . import views

app_name = 'ride'
urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride'),
    path('search_ride/', views.create_ride, name='search_ride'),
]