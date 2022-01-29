from django.urls import path
from . import views

app_name = 'ride'
urlpatterns = [
    path('create_ride/', views.create_ride, name='create_ride'),
    path('search_as_sharer/', views.search_as_sharer, name='search_as_sharer'),
    path('search_as_driver/', views.search_as_driver, name='search_as_driver'),
    path('driver_join/', views.driver_join, name='driver_join'),
    path('sharer_join/', views.sharer_join, name='sharer_join'),
    path('driver_edit/', views.driver_edit, name='driver_edit'),
    path('owner_update/', views.owner_update, name='owner_update'),
    path('sharer_join/', views.sharer_join, name='sharer_join'),
    path('driver_view/', views.driver_view, name='driver_view'),
    path('owner_view/', views.owner_view, name='owner_view'),
    path('sharer_view/', views.sharer_view, name='sharer_view'),
    path('home/', views.home, name='home'),
]
