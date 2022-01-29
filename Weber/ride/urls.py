from django.urls import path
from . import views

app_name = 'ride'
urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride'),
    path('search_as_sharer/', views.search_as_sharer, name='search_as_sharer'),
    path('search_as_rider/', views.search_as_rider, name='search_as_rider'),
    path('home/', views.home, name='home'),
]
