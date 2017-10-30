from django import template
from apps.league.models import Team

register = template.Library()


@register.simple_tag
def get_team_logo(pk):
    """Возвращает логотип команды."""
    team = Team.objects.filter(pk=pk).first()
    if team.logo:
        return team.logo
    return None
