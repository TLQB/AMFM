from django.urls import path

from .import views 

urlpatterns = [
    path("/get_data/", views.TestApi.as_view(), name="test_api"),
]