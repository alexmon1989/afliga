from django.conf.urls import url
from apps.photogallery.views import GalleriesListView, PhotosListView

urlpatterns = [
    url(r'^$', GalleriesListView.as_view(), name='galleries_list'),
    url(r'^(?P<pk>\d+)/$', PhotosListView.as_view(), name='photos_list'),
]
