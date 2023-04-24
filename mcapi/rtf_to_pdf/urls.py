from django.urls import path

from .import views 
from .views import DownloadMediaView

urlpatterns = [
    path("", views.index, name="convert"),
    # path("handle_convert", views.handle_convert, name="handle_convert"),
    path('download-media/', DownloadMediaView.as_view(), name='download_media'),
]