from django.db import models
from apps.league.models import Player


class FooterSettings(models.Model):
    """Настройки футера."""
    information_block_title = models.CharField('Заголовок текстового блока', max_length=100, null=True, blank=True)
    information_block_text = models.TextField('Текст блока (html)', null=True, blank=True)
    contacts_block_html = models.TextField(
        'Текст блока "Контактная информация" (html)',
        null=True,
        blank=True
    )
    facebook_link = models.CharField('Ссылка Facebook', max_length=255, null=True, blank=True)
    vk_link = models.CharField('Ссылка VK', max_length=255, null=True, blank=True)
    twitter_link = models.CharField('Ссылка Twitter', max_length=255, null=True, blank=True)
    google_link = models.CharField('Ссылка Google', max_length=255, null=True, blank=True)
    copyrights_block_html = models.TextField(
        'Текст блока копирайта (html)',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'


class Banner(models.Model):
    """Модель баннера."""
    title = models.CharField('Заголовок', max_length=255, blank=False)
    is_visible = models.BooleanField('Включено', default=True)
    link = models.CharField('Ссылка', max_length=255, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='banners', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class PersonWidget(models.Model):
    """Настройки виджета персоны."""
    title = models.CharField('Заголовок', max_length=255, default='Персона')
    player = models.ForeignKey(Player, verbose_name='Игрок')
    is_visible = models.BooleanField('Включено', default=True)

    class Meta:
        verbose_name = 'Виджет "Персона"'
        verbose_name_plural = 'Виджет "Персона"'


class Analytics(models.Model):
    """Модель HTML-кода аналитики."""
    code = models.TextField('HTML-код')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'HTML-код аналитики'
        verbose_name_plural = 'HTML-код аналитики'
