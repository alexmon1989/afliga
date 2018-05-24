from django.db import models
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


class Gallery(models.Model):
    """Модель галереи."""
    title = models.CharField('Название', max_length=255)
    is_visible = models.BooleanField('Включено', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photos_list', args=[self.pk])

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class Photo(models.Model):
    """Модель фотографии."""
    def upload_to(instance, filename):
        return 'photo-gallery/{}/{}'.format(instance.gallery.pk, filename)

    image = ThumbnailerImageField('Изображение', upload_to=upload_to)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name='Галерея')
    is_visible = models.BooleanField('Включено', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return 'Изображение #{}'.format(self.pk)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
