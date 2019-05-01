from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from apps.league.models import Tournament, Team, Player, Match
import json


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
        context['assistants'] = self.object.get_assistants()
        context['yellow_cards'] = self.object.get_yellow_cards()
        context['red_cards'] = self.object.get_red_cards()
        context['playoff_rounds'] = self.object.get_playoff_rounds()
        context['groups'] = self.object.group_set.all()
        context['playoff_last_rounds'] = self.object.get_playoff_last_rounds()
        context['playoff_future_rounds'] = self.object.get_playoff_future_rounds()
        return context

    @method_decorator(cache_page(None))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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


def get_players(request, team_id):
    """Возвращает JSON с игроками команды."""
    result = list(Player.objects.filter(team_id=int(team_id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")
