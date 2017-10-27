from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Team(models.Model):
    """Модель команды."""
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)
    logo = models.ImageField('Логотип', upload_to='teams', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


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
        return f"players/{instance.team.pk}/{filename}"

    name = models.CharField('ФИО', max_length=255, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда', null=True, blank=True)
    photo = models.ImageField('Фотография', upload_to=upload_to, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Амплуа', null=True, blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    biography = models.TextField('Биография', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Tournament(models.Model):
    """Модель турнира."""
    title = models.CharField('Название турнира', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    players = models.ManyToManyField(Player, through='TournamentPlayer', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'


class TournamentPlayer(models.Model):
    """Модель игрока турнира. Используется для определения какая команда каких игроков заявила на турнир."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Турнир')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда')

    def __str__(self):
        return self.player.name

    class Meta:
        verbose_name = 'Заявка команды на турнир'
        verbose_name_plural = 'Заявки команд на турнир'


class Group(models.Model):
    """Модель группы команд турнира. Может быть как одна группа в турнире (чемпионат), так и несколько (кубок)."""
    title = models.CharField('Название', max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Турнир')
    teams = models.ManyToManyField(Team, blank=True, verbose_name='Команды')
    table = models.TextField('Таблица результатов', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return f"{self.title} в {self.tournament.title}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Match(models.Model):
    """Модель матча."""
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда хозяев', related_name='team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда гостей', related_name='team_2')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа', null=True, blank=True)
    match_date = models.DateTimeField('Время начала матча', blank=True, null=True)
    protocol = models.TextField('Протокол', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return f"{self.team_1} - {self.team_2}"

    def get_score(self):
        """Возвращает счёт матча."""
        if self.match_date > timezone.now():
            return 'Матч ещё не начался'
        goals_team_1 = 0
        goals_team_2 = 0
        goals = self.event_set.filter(pk=1).all()
        for goal in goals:
            if goal.team == self.team_1:
                goals_team_1 += 1
            else:
                goals_team_2 += 1
        return f"{goals_team_1}:{goals_team_2}"

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


class Event(models.Model):
    """Модель события матча."""
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='Тип события')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='Матч')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Команда')
    event_time = models.IntegerField('Минута', validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.event_type} ({self.match})"

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События в матче'
