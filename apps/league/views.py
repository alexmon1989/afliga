from django.views.generic import ListView, DetailView
from apps.league.models import Tournament, Round


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

        # Сортировка таблиц в группах для вывода (по очкам)
        context['groups'] = self.get_object().get_groups_sorted_tables()

        # Последние сыгранные туры
        context['last_rounds'] = Round.get_last_rounds()

        # Последние несыгранные туры
        context['future_rounds'] = Round.get_future_rounds()

        return context
