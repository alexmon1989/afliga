from django.conf.urls import url
from apps.league.views import TournamentListView, TournamentDetailView, TeamDetailView, PlayerDetailView

urlpatterns = [
    url(r'^$', TournamentListView.as_view(), name='tournaments_list'),
    url(r'^tournament/(?P<pk>\d+)/$', TournamentDetailView.as_view(), name='tournament_detail'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^player/(?P<pk>\d+)/$', PlayerDetailView.as_view(), name='player_detail'),
]
