from django.db import models
from django.utils.functional import cached_property
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models import Count
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import json


class Team(models.Model):
    """Модель команды."""
    title = models.CharField('Название', max_length=255)
    city = models.CharField('Город', max_length=255, null=True, blank=True)
    description = RichTextUploadingField('Описание', null=True, blank=True)
    logo = models.ImageField('Логотип', upload_to='teams', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        if self.city:
            return f"{self.title} {self.city}"
        return self.title

    def get_absolute_url(self):
        return reverse('team_detail', args=[self.pk])

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['title']


class Position(models.Model):
    """Модель позиции (амплуа) игрока на поле."""
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Позиция на поле'
        verbose_name_plural = 'Позиции на поле'


class Player(models.Model):
    """Модель игрока."""

    def upload_to(instance, filename):
        return f"players/{instance.pk}/{filename}"

    name = models.CharField('ФИО', max_length=255, blank=False)
    photo = models.ImageField(
        'Фотография',
        upload_to=upload_to,
        null=True, blank=True,
        help_text='Рекомендуемый размер фото: 350px*400px.'
    )
    teams = models.ManyToManyField(Team, verbose_name='Текущие команды')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Амплуа', null=True, blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    biography = RichTextUploadingField('Биография', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        teams = ", ".join([str(t) for t in self.teams.all()])
        if teams:
            return f"{self.name} ({teams})"
        return self.name

    def get_absolute_url(self):
        return reverse('player_detail', args=[self.pk])

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ['name']


class Competition(models.Model):
    """Модель соревнования."""
    title = models.CharField('Название соревнования', max_length=255)
    description = RichTextUploadingField('Описание', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def get_matches_sorted(self):
        """Возвращает матчи соревнования, разбитые на группы и плей-офф"""
        matches = Match.objects.filter(competition=self).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'group__title',
            'match_round__title',
            'match_round__created_at',
        )

        res = {
            'playoff_rounds': [],
            'groups': []
        }

        for match in matches:
            # Групповые матчи
            if match['group__title']:
                # Индекс группы в списке (None, если отсутствует)
                group_index = next(
                    (i for i, item in enumerate(res['groups']) if item['title'] == match['group__title']),
                    None)
                if group_index is None:
                    res['groups'].append({
                        'title': match['group__title'],
                        'rounds': []
                    })
                    group_index = len(res['groups']) - 1

                # Индекс утра в группе (None, если отсутствует)
                round_index = next((i for i, item in enumerate(res['groups'][group_index]['rounds']) if
                                    item['title'] == match['match_round__title']), None)
                if round_index is None:
                    res['groups'][group_index]['rounds'].append({
                        'title': match['match_round__title'],
                        'created_at': match['match_round__created_at'],
                        'matches': []
                    })
                    round_index = len(res['groups'][group_index]['rounds']) - 1

                res['groups'][group_index]['rounds'][round_index]['matches'].append(match)

            # Матчи плей-офф
            else:
                round_index = next(
                    (i for i, item in enumerate(res['playoff_rounds']) if item['title'] == match['match_round__title']),
                    None)
                if round_index is None:
                    res['playoff_rounds'].append({
                        'title': match['match_round__title'],
                        'created_at': match['match_round__created_at'],
                        'matches': []
                    })
                    round_index = len(res['playoff_rounds']) - 1

                res['playoff_rounds'][round_index]['matches'].append(match)

        # Сортировка
        res['playoff_rounds'] = sorted(res['playoff_rounds'], key=lambda x: x['title'])
        res['groups'] = sorted(res['groups'], key=lambda x: x['title'])
        for group in res['groups']:
            group['rounds'] = sorted(group['rounds'], key=lambda x: x['created_at'])

        return res

    def get_playoff_rounds(self):
        """Возвращает список туров турнира."""
        return self.round_set.filter(
            match__group__isnull=True
        ).all()

    def get_playoff_last_rounds(self):
        """Возвращает список туров турнира, в котором есть сыгранные матчи без групп."""
        return self.round_set.filter(
            match__group__isnull=True,
            match__match_date__lte=timezone.now()
        ).order_by('-created_at').all()

    def get_playoff_future_rounds(self):
        """Возвращает список туров турнира, в котором несыгранные матчи без групп."""
        return self.round_set.filter(
            match__group__isnull=True,
            match__match_date__gte=timezone.now()
        ).order_by('created_at').all()

    def get_bombardiers(self):
        """Возвращает список бомбардиров турнира."""
        return Event.objects.filter(
            match__match_round__competition=self,
            event_type=1
        ).values(
            'player'
        ).annotate(
            num_goals=Count('player')
        ).order_by(
            '-num_goals',
            'player__name'
        ).values(
            'player__pk', 'player__name', 'player__photo', 'team__pk', 'team__title', 'team__city', 'team__logo', 'num_goals'
        )

    def get_assistants(self):
        """Возвращает список бомбардиров турнира."""
        return Event.objects.filter(
            match__match_round__competition=self,
            event_type=6
        ).values(
            'player'
        ).annotate(
            num_assistants=Count('player')
        ).order_by(
            '-num_assistants',
            'player__name'
        ).values(
            'player__pk', 'player__name', 'player__photo', 'team__pk', 'team__title', 'team__city', 'team__logo', 'num_assistants'
        )

    def get_yellow_cards(self):
        """Возвращает список штрафников турнира (жёлтые карточки)."""
        return Event.objects.filter(
            match__match_round__competition=self,
            event_type=2
        ).values(
            'player'
        ).annotate(
            num_yellow_cards=Count('player')
        ).order_by(
            '-num_yellow_cards',
            'player__name'
        ).values(
            'player__pk', 'player__name', 'player__photo', 'team__pk', 'team__title', 'team__city', 'team__logo', 'num_yellow_cards'
        )

    def get_red_cards(self):
        """Возвращает список штрафников турнира (красные карточки)."""
        return Event.objects.filter(
            match__match_round__competition=self,
            event_type=3
        ).values(
            'player'
        ).annotate(
            num_red_cards=Count('player')
        ).order_by(
            '-num_red_cards',
            'player__name'
        ).values(
            'player__pk', 'player__name', 'team__pk', 'team__title', 'team__city', 'team__logo', 'num_red_cards'
        )

    def get_teams_id_list(self):
        return self.competitionteamapplication_set.all().values_list('team_id', flat=True)

    @property
    def has_matches(self):
        return self.match_set.count() > 0

    @property
    def has_finished_matches(self):
        return self.match_set.filter(match_date__lt=timezone.now()).count() > 0

    @property
    def has_future_matches(self):
        return self.match_set.filter(match_date__gt=timezone.now()).count() > 0

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('competition_main', args=[self.pk])

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ('-pk',)


class CompetitionTeamApplication(models.Model):
    """Модель заявки команды игроков на соревнования."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда')
    players = models.ManyToManyField(Player, blank=True, verbose_name='Игрок')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Соревнование')

    def __str__(self):
        return self.team.title

    class Meta:
        verbose_name = 'Заявка команды на соревнование'
        verbose_name_plural = 'Заявки команд на соревнования'


class Group(models.Model):
    """Модель группы команд турнира. Может быть как одна группа в турнире (чемпионат), так и несколько (кубок)."""
    title = models.CharField('Название', max_length=255)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Соревнование', null=True)
    teams = models.ManyToManyField(Team, blank=True, verbose_name='Команды')
    table = models.TextField('Таблица результатов', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    def get_sorted_table(self):
        """Возвращает отсортированную по очкам таблицу."""
        teams = dict()
        for team in self.teams.all().values('pk', 'logo'):
            teams[team['pk']] = team['logo']

        table = sorted(json.loads(self.table), key=lambda x: (-x['score'], -(x['goals_scored'] - x['goals_missed'])))
        for item in table:
            item['logo'] = teams[item['id']]
        return table

    def get_rounds(self):
        """Возвращает список туров группы."""
        return Round.objects.filter(
            competition=self.competition,
            match__group=self
        ).order_by('created_at').distinct().all()

    def get_last_rounds(self):
        """Возвращает список туров группы, в которых есть сыгранные матчи."""
        return Round.objects.filter(
            competition=self.competition,
            match__group=self,
            match__match_date__lte=timezone.now()
        ).order_by('-created_at').distinct().all()[:3]

    def get_future_rounds(self):
        """Возвращает список туров группы, в которых есть несыгранные матчи."""
        return Round.objects.filter(
            competition=self.competition,
            match__group=self,
            match__match_date__gte=timezone.now()
        ).order_by('created_at').distinct().all()[:3]

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


@receiver(m2m_changed, sender=Group.teams.through)
def group_save_callback(sender, instance, action, reverse, model, pk_set, *args, **kwargs):
    """Обработчик сигнала изменения поля teams модели Group. Меняет содержимое поля table."""
    data = json.loads(instance.table or '[]')
    if action == 'pre_remove':
        new_data = [x for x in data if x['id'] not in pk_set]
        instance.table = json.dumps(new_data)
        instance.save()
    if action == 'pre_add':
        for pk in pk_set:
            data.append({
                'id': pk,
                'title': Team.objects.filter(pk=pk).first().title,
                'games': 0,
                'wins': 0,
                'draws': 0,
                'defeats': 0,
                'goals_scored': 0,
                'goals_missed': 0,
                'score': 0,
            })
        instance.table = json.dumps(data)
        instance.save()


class Round(models.Model):
    """Модель тура."""
    title = models.CharField('Название', max_length=255, help_text='Например, "4 марта 2017, суббота. 17 Тур"')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Соревнование', null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    def get_matches(self):
        """Возвращает матчи тура."""
        return self.match_set.values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    def get_matches_in_group(self, group):
        """Возвращает матчи тура в конкретной группе."""
        return self.match_set.filter(
            group=group
        ).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    def get_last_matches_in_group(self, group):
        """Возвращает сыгранные матчи тура в конкретной группе."""
        return self.match_set.filter(
            match_date__lte=timezone.now(),
            group=group
        ).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__logo',
            'team_1__city',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    def get_future_matches_in_group(self, group):
        """Возвращает несыгранные матчи тура в конкретной группе."""
        return self.match_set.filter(
            match_date__gte=timezone.now(),
            group=group
        ).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    def get_last_matches(self):
        """Возвращает сыгранные матчи тура."""
        return self.match_set.filter(
            match_date__lte=timezone.now()
        ).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    def get_future_matches(self):
        """Возвращает несыгранные матчи тура."""
        return self.match_set.filter(
            match_date__gte=timezone.now()
        ).values(
            'pk',
            'match_date',
            'goals_team_1',
            'goals_team_2',
            'team_1__pk',
            'team_1__title',
            'team_1__city',
            'team_1__logo',
            'team_2__pk',
            'team_2__title',
            'team_2__city',
            'team_2__logo',
            'is_technical_defeat',
            'youtube_id',
        ).all()

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class Match(models.Model):
    """Модель матча."""
    is_finished = models.BooleanField('Матч окончен', default=False)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Соревнование', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', null=True, blank=True)
    match_round = models.ForeignKey(Round, on_delete=models.CASCADE, verbose_name='Тур')
    match_date = models.DateTimeField('Время начала матча', blank=True, null=True)
    stadium = models.ForeignKey('Stadium', on_delete=models.SET_NULL, verbose_name='Стадион', null=True, blank=True)
    main_referee = models.ForeignKey(
        'Referee',
        on_delete=models.SET_NULL,
        verbose_name='Главный судья',
        null=True,
        blank=True,
        related_name='main_referee'
    )
    other_referees = models.ManyToManyField(
        'Referee', verbose_name='Помощники судьи', blank=True
    )
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда хозяев', related_name='team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда гостей', related_name='team_2')
    coach_team_1 = models.ForeignKey(
        'Coach',
        on_delete=models.SET_NULL,
        verbose_name='Тренер команды 1',
        related_name='coach_team_1',
        null=True,
        blank=True,
    )
    coach_team_2 = models.ForeignKey(
        'Coach',
        on_delete=models.SET_NULL,
        verbose_name='Тренер команды 2',
        related_name='coach_team_2',
        null=True,
        blank=True,
    )
    goals_team_1 = models.PositiveIntegerField('Голов забила команда хозяев', null=True, blank=True, default=None)
    goals_team_2 = models.PositiveIntegerField('Голов забила команда гостей', null=True, blank=True, default=None)
    protocol = RichTextUploadingField('Протокол', blank=True)
    is_technical_defeat = models.BooleanField('Техническое поражение', default=False)
    youtube_id = models.CharField('Id видео на Youtube', null=True, blank=True, default=None, max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return f"{self.team_1} - {self.team_2}"

    def get_score(self):
        """Возвращает счёт матча."""
        return f"{self.get_goals_team_1()}:{self.get_goals_team_2()}"

    def get_goals_team_1(self):
        """Возвращает количество голов, которые забила команда хозяев."""
        if self.match_date and self.match_date > timezone.now():
            return '-'
        if self.goals_team_1:
            return self.goals_team_1
        return 0

    def get_goals_team_2(self):
        """Возвращает количество голов, которые забила команда гостей."""
        if self.match_date and self.match_date > timezone.now():
            return '-'
        if self.goals_team_2:
            return self.goals_team_2
        return 0

    def get_absolute_url(self):
        return reverse('match_summary', args=[self.pk])

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


class EventType(models.Model):
    """Тип события матча (жёлтая карточка, красная карточка, гол)."""
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип события в матче'
        verbose_name_plural = 'Типы событий в матчах'


PERIODS_CHOICES = (
    (1, '1-й тайм'),
    (2, '2-й тайм'),
    (3, 'Дополнительное время'),
)


class Event(models.Model):
    """Модель события матча."""
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='Тип события')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='Матч')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    player_assigned = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        verbose_name='Связанный игрок',
        related_name='player_assigned',
        null=True,
        blank=True,
    )
    period = models.IntegerField('Тайм', choices=PERIODS_CHOICES, null=True, blank=True)
    event_time = models.IntegerField(
        'Минута',
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        default=None
    )
    note = models.CharField('Примечание', null=True, blank=True, max_length=255)

    def __str__(self):
        return f"{self.event_type} ({self.match})"

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События в матче'


class MatchLineup(models.Model):
    """Заявка на матч (протокол)."""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='Матч')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда', null=True, blank=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    start = models.BooleanField('Стартовый состав', default=False)

    def __str__(self):
        return 'Игрок матча'

    class Meta:
        verbose_name = 'Заявка на матч, протокол'
        verbose_name_plural = 'Заявка на матч, протокол'


class Stadium(models.Model):
    """Модель стадиона."""
    title = models.CharField('Название', max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стадион'
        verbose_name_plural = 'Стадионы'


class Referee(models.Model):
    """Модель футбольного судьи."""
    name = models.CharField('ФИО судьи', max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'


class Coach(models.Model):
    """Модель тренера."""
    name = models.CharField('ФИО', max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'
