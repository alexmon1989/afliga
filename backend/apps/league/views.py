from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from apps.league.models import Competition, Team, Player, Match, CompetitionTeamApplication, Group, Round
import json


class TournamentListView(ListView):
    """Отображает страницу со списком турниров."""
    model = Competition
    template_name = 'league/tournaments/list/list.html'
    queryset = Competition.objects.order_by('-created_at')


class TournamentMainView(DetailView):
    """Отображает главную страницу турнира."""
    model = Competition
    template_name = 'league/tournaments/main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playoff_rounds'] = self.object.get_playoff_rounds()
        context['groups'] = self.object.group_set.all().order_by('title')
        context['playoff_last_rounds'] = self.object.get_playoff_last_rounds()
        context['playoff_future_rounds'] = self.object.get_playoff_future_rounds()
        return context


class TournamentTableView(DetailView):
    """Отображает страницу таблицы турнира."""
    model = Competition
    template_name = 'league/tournaments/table/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.object.group_set.all().order_by('title')
        return context


class TournamentCalendarView(DetailView):
    """Отображает страницу календаря турнира."""
    model = Competition
    template_name = 'league/tournaments/calendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['res'] = self.object.get_matches_sorted()
        return context


class TournamentBombardiersView(DetailView):
    """Отображает страницу бомбардиров турнира."""
    model = Competition
    template_name = 'league/tournaments/bombardiers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombardiers'] = self.object.get_bombardiers()
        return context


class TournamentAssistantsView(DetailView):
    """Отображает страницу ассистентов турнира."""
    model = Competition
    template_name = 'league/tournaments/assistants/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assistants'] = self.object.get_assistants()
        return context


class TournamentCardsView(DetailView):
    """Отображает страницу карточек турнира."""
    model = Competition
    template_name = 'league/tournaments/cards/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yellow_cards'] = self.object.get_yellow_cards()
        context['red_cards'] = self.object.get_red_cards()
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


def get_players(request, team_id):
    """Возвращает JSON с игроками команды."""
    result = list(Player.objects.filter(team_id=int(team_id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_players_group(request):
    """Возвращает JSON с игроками команды определённой группы (если она была передана в запросе)."""
    team_id = request.GET.get('team_id')
    group_id = request.GET.get('group_id')

    result = []
    if team_id or group_id:
        qs = CompetitionTeamApplication.objects.all()

        if team_id:
            qs = qs.filter(team_id=team_id)
        if group_id:
            group = Group.objects.get(pk=group_id)
            qs = qs.filter(competition_id=group.tournament_id)
            
        if qs.count():
            result = list(qs.first().players.all().values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_rounds(request, tournament_id=None):
    """Возвращает JSON с турами турнира."""
    res = []
    if tournament_id:
        rounds = Round.objects.filter(competition_id=tournament_id).values('id', 'title')
        if rounds.count() > 0:
            res = list(rounds)
    return HttpResponse(json.dumps(res), content_type="application/json")


def get_groups(request, tournament_id=None):
    """Возвращает JSON с группами турнира."""
    res = []
    if tournament_id:
        groups = Group.objects.filter(competition_id=tournament_id).values('id', 'title')
        if groups.count() > 0:
            res = list(groups)
    return HttpResponse(json.dumps(res), content_type="application/json")


def get_teams(request):
    """Возвращает JSON с коммандами турнира или группы."""
    tournament_id = request.GET.get('tournament_id')
    group_id = request.GET.get('group_id')
    res = []
    if group_id:
        group = Group.objects.get(pk=group_id)
        for team in group.teams.all():
            res.append({'id': team.id, 'title': team.title})
    elif tournament_id:
        tournament = Competition.objects.get(pk=tournament_id)
        applications = tournament.tournamentteamapplication_set.all()
        for app in applications:
            res.append({'id': app.team.id, 'title': app.team.title})
    if res:
        res = list(res)
    return HttpResponse(json.dumps(res), content_type="application/json")
