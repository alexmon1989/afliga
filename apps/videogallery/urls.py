from django.conf.urls import url
from apps.videogallery.views import VideosListView

urlpatterns = [
    url(r'^$', VideosListView.as_view(), name='videos_list'),
]
