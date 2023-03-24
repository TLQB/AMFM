from django.urls import path
from .import mqtt 
from .import views 

urlpatterns = [
    path("/map/", views.map, name="map"),
    # path("/map/get_location/", views.get_location, name="map"),
    path('ajax/get_location/', mqtt.get_location, name='get_location'),
]