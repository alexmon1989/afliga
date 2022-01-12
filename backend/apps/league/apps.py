from django.apps import AppConfig


class LeagueConfig(AppConfig):
    name = 'apps.league'
    verbose_name = 'Футбольная лига'

    def ready(self):
        import apps.league.signals
