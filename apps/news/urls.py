from django.conf.urls import url
from apps.news.views import NewsList

urlpatterns = [
    url(r'^$', NewsList.as_view(), name='news_list'),
]
