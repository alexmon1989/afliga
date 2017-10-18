from django.conf.urls import url
from apps.contacts.views import ContactView

urlpatterns = [
    url(r'^$', ContactView.as_view(), name='contacts'),
]
