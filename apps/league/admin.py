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


class EventInline(admin.TabularInline):
    model = Event
    extra = 2
    exclude = ('table',)


class MatchForm(forms.ModelForm):
    """Класс формы для редактирования матча."""
    recount_results = forms.BooleanField(
        label='Пересчитать результаты в таблице группы',
        required=False,
        help_text='Если это групповой матч, то произведётся пересчёт очков у команд. '
                  'Также можно отредактировать вручную, '
                  'для этого необходимо перейти в интерфейс администрирования группы.'
    )

    def save(self, commit=True):
        """Сохранение данных формы."""
        recount_results = self.cleaned_data.get('recount_results', False)
        # Если необходимо пересчитать результаты в таблице группы
        if recount_results:
            if self.instance.group:
                group_teams = self.instance.group.teams.all()
                team_1 = self.instance.team_1
                team_2 = self.instance.team_2
                if team_1 in group_teams and team_2 in group_teams:
                    group_data = json.loads(self.instance.group.table)

                    goals_team_1 = self.instance.get_goals_team_1()
                    goals_team_2 = self.instance.get_goals_team_2()

                    for item in group_data:
                        # Пересчёт результатов команды хозяев
                        if item['id'] == team_1.pk:
                            item['goals_scored'] += goals_team_1
                            item['goals_missed'] += goals_team_2
                            item['games'] += 1
                            if goals_team_1 > goals_team_2:
                                item['wins'] += 1
                                item['score'] += 3
                            elif goals_team_1 == goals_team_2:
                                item['draws'] += 1
                                item['score'] += 1
                            else:
                                item['defeats'] += 1

                        # Пересчёт результатов команды гостей
                        if item['id'] == team_2.pk:
                            item['goals_scored'] += goals_team_2
                            item['goals_missed'] += goals_team_1
                            item['games'] += 1
                            if goals_team_2 > goals_team_1:
                                item['wins'] += 1
                                item['score'] += 3
                            elif goals_team_1 == goals_team_2:
                                item['draws'] += 1
                                item['score'] += 1
                            else:
                                item['defeats'] += 1

                    # Сохранение обновлённой таблицы
                    self.instance.group.table = json.dumps(group_data)
                    self.instance.group.save()

        return super(MatchForm, self).save(commit=commit)


@admin.register(Match)
class MatchesAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования матчей."""
    form = MatchForm
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
