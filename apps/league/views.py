from django.views.generic import ListView, DetailView
from apps.league.models import Tournament, Team, Player


class TournamentListView(ListView):
    """Отображает страницу со списком турниров."""
    model = Tournament
    template_name = 'league/tournaments/list/list.html'
    queryset = Tournament.objects.order_by('-created_at')


class TournamentDetailView(DetailView):
    """Отображает страницу с деталями турнира."""
    model = Tournament
    template_name = 'league/tournaments/detail/detail.html'


class TeamDetailView(DetailView):
    """Отображает страницу с деталями команды."""
    model = Team
    template_name = 'league/teams/detail.html'


class PlayerDetailView(DetailView):
    """Отображает страницу с деталями игрока."""
    model = Player
    template_name = 'league/players/detail.html'
