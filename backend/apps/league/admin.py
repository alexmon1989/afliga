from django.contrib import admin
from django import forms
import json
from apps.league.models import (Team, Player, Position, Competition, Group, Match, Event, EventType, Round,
                                CompetitionTeamApplication, MatchLineup, Stadium, Referee, Coach, Season)
from json import JSONDecodeError
from django.contrib.admin.options import BaseModelAdmin
from django.db.models.constants import LOOKUP_SEP


class AdminBaseWithSelectRelated(BaseModelAdmin):
    """
    Admin Base using list_select_related for get_queryset related fields
    """
    list_select_related = []
    list_prefetch_related = []

    def get_queryset(self, request):
        return super(AdminBaseWithSelectRelated, self).get_queryset(request).select_related(*self.list_select_related).prefetch_related(*self.list_prefetch_related)

    def form_apply_select_related(self, form):
        for related_field in self.list_select_related:
            splitted = related_field.split(LOOKUP_SEP)
            if len(splitted) > 1:
                field = splitted[0]
                related = LOOKUP_SEP.join(splitted[1:])
                try:
                    form.base_fields[field].queryset = form.base_fields[field].queryset.select_related(related)
                except KeyError:
                    pass

    def form_apply_prefetch_related(self, form):
        for related_field in self.list_prefetch_related:
            splitted = related_field.split(LOOKUP_SEP)
            if len(splitted) > 1:
                field = splitted[0]
                related = LOOKUP_SEP.join(splitted[1:])
                try:
                    form.base_fields[field].queryset = form.base_fields[field].queryset.prefetch_related(related)
                except KeyError:
                    pass


class AdminInlineWithSelectRelated(admin.StackedInline, AdminBaseWithSelectRelated):
    """
    Admin Inline using list_select_related for get_queryset and get_formset related fields
    """

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(AdminInlineWithSelectRelated, self).get_formset(request, obj, **kwargs)
        self.form_apply_select_related(formset.form)
        self.form_apply_prefetch_related(formset.form)
        return formset


class AdminTabularInlineWithSelectRelated(admin.TabularInline, AdminBaseWithSelectRelated):
    """
    Admin Inline using list_select_related for get_queryset and get_formset related fields
    """

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(AdminTabularInlineWithSelectRelated, self).get_formset(request, obj, **kwargs)
        self.form_apply_select_related(formset.form)
        self.form_apply_prefetch_related(formset.form)
        return formset


class AdminWithSelectRelated(admin.ModelAdmin, AdminBaseWithSelectRelated):
    """
    Admin using list_select_related for get_queryset and get_form related fields
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminWithSelectRelated, self).get_form(request, obj, **kwargs)
        self.form_apply_select_related(form)
        self.form_apply_prefetch_related(form)
        return form


class FilterWithSelectRelated(admin.RelatedFieldListFilter):
    list_select_related = []

    def field_choices(self, field, request, model_admin):
        return [
            (getattr(x, field.remote_field.get_related_field().attname), str(x))
            for x in self.get_queryset(field)
        ]

    def get_queryset(self, field):
        return field.remote_field.model._default_manager.select_related(*self.list_select_related)


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования возможных позиций игроков."""
    ordering = ('title',)
    search_fields = ('title',)


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования команд."""
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)


@admin.register(Player)
class PlayersAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования игроков."""
    list_display = ('name', 'get_teams', 'position', 'birth_date', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('position',)
    list_select_related = ('position',)
    autocomplete_fields = ['teams']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('teams')

    def get_teams(self, obj):
        return ", ".join([str(t) for t in obj.teams.all()])

    get_teams.short_description = 'Текущие команды'


class CompetitionTeamApplicationInline(AdminInlineWithSelectRelated):
    model = CompetitionTeamApplication
    extra = 0
    filter_horizontal = ('players',)
    list_prefetch_related = (
        'players',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(CompetitionTeamApplicationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "team" and hasattr(self, "cached_teams"):
            field.choices = self.cached_teams
        return field

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super(CompetitionTeamApplicationInline, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "players" and hasattr(self, "cached_players"):
            field.choices = self.cached_players
        return field


class GroupInline(AdminInlineWithSelectRelated):
    model = Group
    extra = 0
    exclude = ('table',)
    filter_horizontal = ('teams',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super(GroupInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "teams" and hasattr(self, "cached_teams_for_groups"):
            field.choices = self.cached_teams_for_groups
        return field

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['teams'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        return formset


@admin.register(Competition)
class CompetitionsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования соревнований."""
    list_display = ('title', 'season', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('season')

    def get_inline_instances(self, request, obj=None):
        # Показывать GroupInline только если соревнование уже создано
        if obj:
            self.inlines = (GroupInline, CompetitionTeamApplicationInline)
        else:
            self.inlines = (CompetitionTeamApplicationInline,)

        return super().get_inline_instances(request, obj)

    def get_formsets_with_inlines(self, request, obj=None):
        if obj:
            teams_for_groups = Team.objects.filter(pk__in=obj.get_teams_id_list())
        teams_all = Team.objects.all()
        players = Player.objects.prefetch_related('teams')

        # "Кеширование" элементов для ускорения
        for inline in self.get_inline_instances(request, obj):
            inline.cached_players = [(i.pk, str(i)) for i in players]
            inline.cached_teams = [(i.pk, str(i)) for i in teams_all]
            inline.cached_teams.insert(0, ("", "---------"))
            if obj:
                inline.cached_teams_for_groups = [(i.pk, str(i)) for i in teams_for_groups]
                inline.cached_teams_for_groups.insert(0, ("", "---------"))
            yield inline.get_formset(request, obj), inline


class GroupForm(forms.ModelForm):
    """Класс формы для редактирования группы."""
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        if self.instance.table:
            self.initial['table'] = json.dumps(
                json.loads(self.instance.table),
                ensure_ascii=False,
                sort_keys=True,
                indent=2
            )

    def clean_table(self):
        data = self.cleaned_data['table']
        try:
            json.loads(data)
        except JSONDecodeError as e:
            raise forms.ValidationError("Неверный формат данных: {}".format(e))
        return data


@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования групп."""
    form = GroupForm
    list_display = ('title', 'competition', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title', 'competition')
    list_filter = ('competition',)


class EventInline(AdminInlineWithSelectRelated):
    model = Event
    extra = 0
    exclude = ('table',)
    list_select_related = (
        'team',
        'player',
        'player_assigned',
        'event_type',
        'match__team_1',
        'match__team_2',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(EventInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "team" and hasattr(self, "cached_teams"):
            field.choices = self.cached_teams
        elif (db_field.name == "player" or db_field.name == "player_assigned") and hasattr(self, "cached_players"):
            field.choices = self.cached_players
        return field

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super(EventInline, self).formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ('team', 'player'):
            formfield.widget.can_add_related = False
        return formfield


class LineupInline(AdminTabularInlineWithSelectRelated):
    model = MatchLineup
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(LineupInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "team" and hasattr(self, "cached_teams"):
            field.choices = self.cached_teams
        if db_field.name == "player" and hasattr(self, "cached_players"):
            field.choices = self.cached_players
        return field

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super(LineupInline, self).formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ('team', 'player'):
            formfield.widget.can_add_related = False
        return formfield


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
class MatchesAdmin(AdminWithSelectRelated):
    """Класс для описания интерфейса администрирования матчей."""
    autocomplete_fields = ('stadium', 'main_referee', 'other_referees', 'coach_team_1', 'coach_team_2',)
    save_on_top = True
    form = MatchForm
    list_display = ('teams', 'score', 'match_round', 'competition', 'group', 'match_date', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('team_1', 'team_2', 'competition')
    list_select_related = [
        'competition',
        'group__competition',
        'match_round__competition',
        'team_1',
        'team_2',
        'stadium',
    ]

    def get_inline_instances(self, request, obj=None):
        if obj:
            self.inlines = (
                LineupInline,
                EventInline,
            )
        return super().get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                ('Неизменяемые данные', {
                    'fields': (
                        'competition',
                        'match_round',
                        'group',
                        'team_1',
                        'team_2',
                    )
                }),
                ('Детальная информация о матче', {
                    'fields': (
                        'is_finished',
                        'match_date',
                        'stadium',
                        'main_referee',
                        'other_referees',
                        'coach_team_1',
                        'coach_team_2',
                        'goals_team_1',
                        'goals_team_2',
                        'youtube_id',
                        'is_technical_defeat',
                        'protocol',
                        'recount_results',
                    )
                }),
            )

        return ((None, {
            'fields': (
                'competition',
                'match_round',
                'group',
                'team_1',
                'team_2',
            )
        })),

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'competition',
                'match_round',
                'group',
                'team_1',
                'team_2',
            ]
        return []

    def teams(self, obj):
        return f"{obj.team_1} - {obj.team_2}"
    teams.short_description = 'Команды'

    def score(self, obj):
        return f"{obj.get_score()}"
    score.short_description = 'Счёт'

    def get_formsets_with_inlines(self, request, obj=None):
        if obj:
            teams = Team.objects.filter(pk__in=[obj.team_1.pk, obj.team_2.pk, ])
            players = Player.objects.filter(
                competitionteamapplication__team_id__in=[obj.team_1.pk, obj.team_2.pk,]
            ).prefetch_related('teams').all()

            # "Кеширование" элементов для ускорения
            for inline in self.get_inline_instances(request, obj):
                inline.cached_teams = [(i.pk, str(i)) for i in teams]
                inline.cached_teams.insert(0, ("", "---------"))
                inline.cached_players = [(i.pk, str(i)) for i in players]
                inline.cached_players.insert(0, ("", "---------"))
                yield inline.get_formset(request, obj), inline

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super(MatchesAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ('team_1', 'team_2'):
            formfield.widget.can_add_related = False
        return formfield


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования типов событий."""
    ordering = ('title',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования туров."""
    list_display = ('title', 'competition', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('competition',)
    search_fields = ('title', 'competition')


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования стадионов."""
    list_display = ('title', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title',)


@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования судей."""
    list_display = ('name', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('name',)


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования тренеров."""
    list_display = ('name', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('name',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования сезонов."""
    list_display = ('title', 'sponsor', 'is_current_season', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('title',)
    list_editable = ('is_current_season', )
