from django.urls import path
from . import views

app_name = 'ride'
urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride'),
    path('search_as_sharer/', views.search_as_sharer, name='search_as_sharer'),
    path('search_as_driver/', views.search_as_driver, name='search_as_driver'),
    path('driver_join/<int:ride_id>/', views.driver_join, name='driver_join'),
    path('sharer_join/<int:ride_id>/', views.sharer_join, name='sharer_join'),
    path('driver_edit/<int:ride_id>/', views.driver_edit, name='driver_edit'),
    path('owner_edit/<int:ride_id>/', views.owner_edit, name='owner_edit'),
    path('sharer_join/<int:ride_id>/', views.sharer_join, name='sharer_join'),
    path('driver_view/<int:ride_id>/', views.driver_view, name='driver_view'),
    path('owner_view/<int:ride_id>/', views.owner_view, name='owner_view'),
    path('sharer_view/', views.sharer_view, name='sharer_view'),
    path('home/', views.home, name='home'),
]
