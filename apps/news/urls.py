from django.conf.urls import url
from apps.news.views import NewsListView, NewsDetailView

urlpatterns = [
    url(r'^$', NewsListView.as_view(), name='news_list'),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news_detail'),
]
