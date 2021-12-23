from django.conf.urls import url
from django.urls import path
from apps.league.views import (CompetitionListView, TeamDetailView, PlayerDetailView,  MatchSummaryView,
                               MatchLineupView, get_players, get_players_competition, get_rounds, get_groups, get_teams,
                               CompetitionMainView, CompetitionTableView, CompetitionCalendarView,
                               CompetitionBombardiersView, CompetitionAssistantsView, CompetitionCardsView)

urlpatterns = [
    url(r'^$', CompetitionListView.as_view(), name='competitions_list'),

    path('competition/<int:pk>/', CompetitionMainView.as_view(), name='competition_main'),
    path('competition/<int:pk>/table/', CompetitionTableView.as_view(), name='competition_table'),
    path('competition/<int:pk>/calendar/', CompetitionCalendarView.as_view(), name='competition_calendar'),
    path('competition/<int:pk>/bombardiers/', CompetitionBombardiersView.as_view(), name='competition_bombardiers'),
    path('competition/<int:pk>/assistants/', CompetitionAssistantsView.as_view(), name='competition_assistants'),
    path('competition/<int:pk>/cards/', CompetitionCardsView.as_view(), name='competition_cards'),

    url(r'^team/(?P<pk>\d+)$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^player/(?P<pk>\d+)$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^match/(?P<pk>\d+)$', MatchSummaryView.as_view(), name='match_summary'),
    url(r'^match/(?P<pk>\d+)/lineup/$', MatchLineupView.as_view(), name='match_lineup'),
    url(r'^get-players/(?P<team_id>\d+)$', get_players, name='get_players'),
    path(r'get-rounds/<int:competition_id>/', get_rounds, name='get_rounds'),
    path(r'get-groups/<int:competition_id>/', get_groups, name='get_groups'),
    path(r'get-teams/', get_teams, name='get_teams'),
    path(
        'get-players-competition/',
        get_players_competition,
        name='get_players_group'
    ),
]
