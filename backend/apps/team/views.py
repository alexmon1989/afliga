from django.views.generic import ListView
from apps.team.models import TeamMember


class TeamListView(ListView):
    """Отображает страницу со списком сотрудников."""
    model = TeamMember
    template_name = 'team/list.html'

    def get_queryset(self):
        return TeamMember.objects.filter(is_visible=True).order_by('created_at')
