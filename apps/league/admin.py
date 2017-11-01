from django.contrib import admin
from django import forms
import json
from apps.league.models import (Team, Player, Position, Tournament, Group, Match, TournamentPlayer, Event, EventType,
                                Round)


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования возможных позиций игроков."""
    ordering = ('title',)
    search_fields = ('title',)


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования команд."""
    list_display = ('title', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title',)


@admin.register(Player)
class PlayersAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования игроков."""
    list_display = ('name', 'team', 'position', 'birth_date', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title', 'team')
    list_filter = ('team', 'position')


class TournamentPlayerInline(admin.TabularInline):
    model = TournamentPlayer
    extra = 1


class GroupInline(admin.StackedInline):
    model = Group
    extra = 1
    exclude = ('table',)


@admin.register(Tournament)
class TournamentsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования турниров."""
    list_display = ('title', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title',)
    inlines = (GroupInline, TournamentPlayerInline,)


class GroupForm(forms.ModelForm):
    """Класс формы для редактирования группы."""
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.initial['table'] = json.dumps(
            json.loads(self.instance.table),
            ensure_ascii=False,
            sort_keys=True,
            indent=2
        )


@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования групп."""
    form = GroupForm
    list_display = ('title', 'tournament', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title', 'tournament')
    list_filter = ('tournament',)


class EventInline(admin.StackedInline):
    model = Event
    extra = 2
    exclude = ('table',)


@admin.register(Match)
class MatchesAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования матчей."""
    list_display = ('teams', 'score', 'match_round', 'group', 'tournament', 'match_date', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = (EventInline,)
    list_filter = ('team_1', 'team_2', 'match_round__tournament__title')

    def teams(self, obj):
        return f"{obj.team_1} - {obj.team_2}"
    teams.short_description = 'Команды'

    def tournament(self, obj):
        return f"{obj.match_round.tournament}"
    tournament.short_description = 'Турнир'

    def score(self, obj):
        return f"{obj.get_score()}"
    score.short_description = 'Счёт'


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования типов событий."""
    ordering = ('title',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования туров."""
    list_display = ('title', 'tournament', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('tournament',)
    search_fields = ('title', 'tournament')
