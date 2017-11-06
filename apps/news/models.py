from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    """Модель новости."""
    title = models.CharField('Заголовок', max_length=255, blank=False)
    text = RichTextUploadingField('Текст', blank=False)
    is_visible = models.BooleanField('Включено', default=True)
    image = models.ImageField(
        'Изображение',
        upload_to='news',
        null=True,
        blank=True,
        help_text='Оптимальный размер: 740px*380px.'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
