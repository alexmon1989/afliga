from django.db import models


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
