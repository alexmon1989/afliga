from django import template
from apps.league.models import Team, Match

register = template.Library()


@register.simple_tag
def get_team_logo(pk):
    """Возвращает логотип команды."""
    team = Team.objects.filter(pk=pk).first()
    if team and team.logo:
        return team.logo
    return None


@register.simple_tag
def get_last_matches_in_group(round, group):
    """Возвращает сыгранные матчи тура в конкретной группе."""
    return round.get_last_matches_in_group(group)


@register.simple_tag
def get_future_matches_in_group(round, group):
    """Возвращает несыгранные матчи тура в конкретной группе."""
    return round.get_future_matches_in_group(group)


@register.simple_tag
def get_matches_in_group(round, group):
    """Возвращает матчи тура в конкретной группе."""
    return round.get_matches_in_group(group)


@register.simple_tag
def get_matches(round):
    """Возвращает матчи тура."""
    return round.get_matches()


@register.inclusion_tag('league/tournaments/templatetags/match_tr.html')
def match_tr(match):
    return {'match': match}


@register.simple_tag
def get_match_score(match):
    """Возвращает счёт матча."""
    team_1_goals = 0
    if match['goals_team_1']:
        team_1_goals = match['goals_team_1']
    team_2_goals = 0
    if match['goals_team_2']:
        team_2_goals = match['goals_team_2']
    return f"{team_1_goals}:{team_2_goals}"
