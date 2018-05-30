from django.views.generic import ListView, DetailView
from apps.league.models import Tournament, Team, Player, Match


class TournamentListView(ListView):
    """Отображает страницу со списком турниров."""
    model = Tournament
    template_name = 'league/tournaments/list/list.html'
    queryset = Tournament.objects.order_by('-created_at')


class TournamentDetailView(DetailView):
    """Отображает страницу с деталями турнира."""
    model = Tournament
    template_name = 'league/tournaments/detail/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombardiers'] = self.object.get_bombardiers()
        return context


class TeamDetailView(DetailView):
    """Отображает страницу с деталями команды."""
    model = Team
    template_name = 'league/teams/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['players'] = self.get_object().player_set.order_by('position').all()
        return context


class PlayerDetailView(DetailView):
    """Отображает страницу с деталями игрока."""
    model = Player
    template_name = 'league/players/detail.html'


class MatchDetailView(DetailView):
    """Отображает страницу с деталями матча."""
    model = Match
    template_name = 'league/match/detail.html'
