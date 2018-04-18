from django.db import models
from apps.league.models import Tournament


class Carousel(models.Model):
    """Модель слайдера."""
    title = models.CharField('Заголовок', max_length=255)
    under_title = models.CharField('Текст под заголовком', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='carousel', help_text='Рекомендуемый размер: 1140px*400px')
    link = models.CharField('Ссылка', max_length=255, blank=True, null=True)
    is_visible = models.BooleanField('Включено', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'


class LastTournament(models.Model):
    """Модель блока последнего турнира."""
    tournament = models.ForeignKey(Tournament, blank=True, null=True, verbose_name='Турнир', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'


class BombardiersPenaltiesTableSettings(models.Model):
    """Модель настроек блоков "Бомабардиры", "Штрафники" и "Таблица"."""
    tournament = models.ForeignKey(Tournament, verbose_name='Турнир', on_delete=models.CASCADE)
    show_table = models.BooleanField('Показывать турнирную таблицу', default=True)
    show_bombardiers = models.BooleanField('Показывать бомбардиров', default=True)
    show_penalties = models.BooleanField('Показывать штрафников', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Таблица, бомбардиры, штрафники'
        verbose_name_plural = 'Таблица, бомбардиры, штрафники'
