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


@register.inclusion_tag('league/competitions/templatetags/match_tr.html')
def match_tr(match):
    return {'match': match}


@register.simple_tag
def get_match_score(pk):
    """Возвращает счёт матча."""
    return Match.objects.filter(pk=pk).first().get_score()


@register.filter
def shorten_name(name):
    """Возвращает счёт матча."""
    name_list = name.split()
    if len(name_list) > 1:
        return f"{name_list[0]} {name_list[1][0]}."
    return name_list[0]

