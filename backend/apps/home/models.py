from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from apps.league.models import Competition


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


class LastCompetition(models.Model):
    """Модель блока последнего турнира."""
    competition = models.ForeignKey(Competition, blank=True, null=True, verbose_name='Соревнование',
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'


class WidgetsSettings(models.Model):
    """Модель настроек блоков "Бомабардиры", "Ассистенты", "Штрафники" и "Таблица"."""
    competition = models.ForeignKey(Competition, verbose_name='Соревнование', on_delete=models.CASCADE, null=True)
    show_table = models.BooleanField('Показывать турнирную таблицу', default=True)
    show_bombardiers = models.BooleanField('Показывать бомбардиров', default=True)
    show_penalties = models.BooleanField('Показывать штрафников', default=True)
    show_assistants = models.BooleanField('Показывать ассистентов', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Виджеты'
        verbose_name_plural = 'Виджеты'


@receiver(post_save)
def clear_the_cache(**kwargs):
    """Очистка кеша при сохранении моделей."""
    cache.clear()
