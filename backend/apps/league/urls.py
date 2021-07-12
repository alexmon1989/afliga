from django.conf.urls import url
from django.urls import path
from apps.league.views import (TournamentListView, TeamDetailView, PlayerDetailView,  MatchDetailView, get_players,
                               get_players_group, get_rounds, get_groups, get_teams, TournamentMainView,
                               TournamentTableView, TournamentCalendarView, TournamentBombardiersView,
                               TournamentAssistantsView, TournamentCardsView)

urlpatterns = [
    url(r'^$', TournamentListView.as_view(), name='tournaments_list'),

    path('competition/<int:pk>/', TournamentMainView.as_view(), name='competition_main'),
    path('competition/<int:pk>/table/', TournamentTableView.as_view(), name='competition_table'),
    path('competition/<int:pk>/calendar/', TournamentCalendarView.as_view(), name='competition_calendar'),
    path('competition/<int:pk>/bombardiers/', TournamentBombardiersView.as_view(), name='competition_bombardiers'),
    path('competition/<int:pk>/assistants/', TournamentAssistantsView.as_view(), name='competition_assistants'),
    path('competition/<int:pk>/cards/', TournamentCardsView.as_view(), name='competition_cards'),

    url(r'^team/(?P<pk>\d+)$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^player/(?P<pk>\d+)$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^match/(?P<pk>\d+)$', MatchDetailView.as_view(), name='match_detail'),
    url(r'^get-players/(?P<team_id>\d+)$', get_players, name='get_players'),
    path(r'get-rounds/<int:tournament_id>/', get_rounds, name='get_rounds'),
    path(r'get-groups/<int:tournament_id>/', get_groups, name='get_groups'),
    path(r'get-teams/', get_teams, name='get_teams'),
    path(
        'get-players-group/',
        get_players_group,
        name='get_players_group'
    ),
]
