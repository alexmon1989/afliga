from django.conf.urls import url
from apps.league.views import TournamentListView, TournamentDetailView

urlpatterns = [
    url(r'^$', TournamentListView.as_view(), name='tournaments_list'),
    url(r'^tournament/(?P<pk>\d+)/$', TournamentDetailView.as_view(), name='tournament_detail'),
]