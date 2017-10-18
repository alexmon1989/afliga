from django.db import models


class Contact(models.Model):
    """Модель данных страницы контактов."""
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Текст', max_length=1024)
    phones = models.TextField('Телефон(ы)', max_length=255)
    emails = models.TextField('E-Mail(ы)', max_length=255)

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"
