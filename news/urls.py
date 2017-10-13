from django.conf.urls import url
from news.views import NewsList

urlpatterns = [
    url(r'^$', NewsList.as_view(), name='news_list'),
]
