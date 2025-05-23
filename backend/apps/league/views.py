from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from apps.league.models import Competition, Team, Player, Match, Group, Round
import apps.league.services as services
from afliga.utils import calculate_age
import json


class CompetitionListView(ListView):
    """Отображает страницу со списком турниров."""
    model = Competition
    template_name = 'league/competitions/list/list.html'
    queryset = Competition.objects.select_related('season').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competitions'] = services.competition_get_competitions_list(self.get_queryset())
        return context


class CompetitionBaseView(DetailView):
    model = Competition

    def get_queryset(self):
        return super().get_queryset().select_related('season')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competition_full_title'] = services.competition_get_full_title(self.object)
        return context


class CompetitionMainView(CompetitionBaseView):
    """Отображает главную страницу турнира."""
    template_name = 'league/competitions/main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playoff_rounds'] = self.object.get_playoff_rounds()
        context['groups'] = self.object.group_set.all().order_by('title')
        context['playoff_last_rounds'] = self.object.get_playoff_last_rounds()
        context['playoff_future_rounds'] = self.object.get_playoff_future_rounds()
        return context


class CompetitionTableView(CompetitionBaseView):
    """Отображает страницу таблицы турнира."""
    template_name = 'league/competitions/table/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.object.group_set.all().order_by('title')
        return context


class CompetitionCalendarView(CompetitionBaseView):
    """Отображает страницу календаря турнира."""
    template_name = 'league/competitions/calendar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['res'] = self.object.get_matches_sorted()
        return context


class CompetitionBombardiersView(CompetitionBaseView):
    """Отображает страницу бомбардиров турнира."""
    template_name = 'league/competitions/bombardiers/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombardiers'] = self.object.get_bombardiers()
        return context


class CompetitionAssistantsView(CompetitionBaseView):
    """Отображает страницу ассистентов турнира."""
    template_name = 'league/competitions/assistants/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assistants'] = services.competition_get_assistants(self.object.pk)
        return context


class CompetitionCardsView(CompetitionBaseView):
    """Отображает страницу карточек турнира."""
    template_name = 'league/competitions/cards/index.html'

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

        # Турниры текущего сезона, где есть команда
        context['competitions'] = services.competition_get_current_season_items_with_team(self.object.pk)

        return context


class PlayerDetailView(DetailView):
    """Отображает страницу с деталями игрока."""
    model = Player
    template_name = 'league/players/detail.html'
    queryset = Player.objects.prefetch_related('teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Текущие команды игрока
        context['player_teams'] = services.player_get_player_teams(self.object.id)
        if self.object.birth_date:
            context['player_age'] = calculate_age(self.object.birth_date)

        # Карьера игрока
        context['player_career'] = services.player_get_career(self.object.id)

        return context


class MatchSummaryView(DetailView):
    """Отображает страницу с деталями матча."""
    model = Match
    template_name = 'league/match/summary/index.html'

    def get_queryset(self):
        return Match.objects.prefetch_related('other_referees').select_related(
            'match_round__competition',
            'team_1',
            'team_2',
            'stadium',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # События матча
        match_events = services.match_get_all_events(self.object)

        # События матча без лучших игроков
        context['match_main_events'] = services.match_get_main_events(match_events)

        # Лучшие игроки матча
        context['match_best_players_team_1'] = services.match_get_best_players(match_events, self.object.team_1_id)
        context['match_best_players_team_2'] = services.match_get_best_players(match_events, self.object.team_2_id)

        return context


class MatchLineupView(DetailView):
    """Отображает страницу с составом игроков на матч."""
    model = Match
    template_name = 'league/match/lineup/index.html'

    def get_queryset(self):
        return Match.objects.prefetch_related('other_referees').select_related(
            'match_round__competition',
            'team_1',
            'team_2',
            'stadium',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # События матча
        match_events = services.match_get_all_events(self.object)

        # # Составы на матч
        match_lineup = services.match_get_lineup(self.object, match_events)
        context['match_lineup_start_team_1'] = services.match_get_lineup_start_team(match_lineup, self.object.team_1_id)
        context['match_lineup_start_team_2'] = services.match_get_lineup_start_team(match_lineup, self.object.team_2_id)
        context['match_lineup_reserve_team_1'] = services.match_get_lineup_reserve_team(
            match_lineup,
            self.object.team_1_id
        )
        context['match_lineup_reserve_team_2'] = services.match_get_lineup_reserve_team(
            match_lineup,
            self.object.team_2_id
        )

        return context


def get_players(request, team_id):
    """Возвращает JSON с игроками команды."""
    result = list(Player.objects.filter(team_id=int(team_id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_players_competition(request):
    """Возвращает JSON с игроками команды, заявленными на определённый турнир."""
    team_id = request.GET.get('team_id')
    competition_id = request.GET.get('competition_id')

    result = []
    if team_id and competition_id:
        result = list(Player.objects.filter(
            competitionteamapplication__competition=competition_id,
            competitionteamapplication__team_id=team_id
        ).values('id', 'name'))

    return HttpResponse(json.dumps(result), content_type="application/json")


def get_rounds(request, competition_id=None):
    """Возвращает JSON с турами турнира."""
    res = []
    if competition_id:
        rounds = Round.objects.filter(competition_id=competition_id).values('id', 'title')
        if rounds.count() > 0:
            res = list(rounds)
    return HttpResponse(json.dumps(res), content_type="application/json")


def get_groups(request, competition_id=None):
    """Возвращает JSON с группами турнира."""
    res = []
    if competition_id:
        groups = Group.objects.filter(competition_id=competition_id).values('id', 'title')
        if groups.count() > 0:
            res = list(groups)
    return HttpResponse(json.dumps(res), content_type="application/json")


def get_teams(request):
    """Возвращает JSON с командами турнира или группы."""
    competition_id = request.GET.get('competition_id')
    group_id = request.GET.get('group_id')
    res = []
    if group_id:
        group = Group.objects.get(pk=group_id)
        for team in group.teams.all():
            res.append({'id': team.id, 'title': team.title})
    elif competition_id:
        competition = Competition.objects.get(pk=competition_id)
        applications = competition.competitionteamapplication_set.all()
        for app in applications:
            res.append({'id': app.team.id, 'title': app.team.title})
    if res:
        res = list(res)
    return HttpResponse(json.dumps(res), content_type="application/json")
