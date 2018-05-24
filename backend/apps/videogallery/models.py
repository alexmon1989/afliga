from django.db import models


class Video(models.Model):
    """Модель видео."""
    title = models.CharField('Название', max_length=255)
    youtube_id = models.CharField('Youtube ID', max_length=255)
    is_visible = models.BooleanField('Включено', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
