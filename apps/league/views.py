from django.views.generic import ListView, DetailView
from apps.league.models import Tournament


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
        context = super(TournamentDetailView, self).get_context_data(**kwargs)
        return context
