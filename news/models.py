from django.db import models


class News(models.Model):
    """Модель новости."""
    title = models.CharField('Заголовок', max_length=255, blank=False)
    text = models.TextField('Текст', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
