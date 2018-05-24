from django.db import models


class TeamMember(models.Model):
    """Модель для описания члена команды."""
    name = models.CharField('ФИО', max_length=255)
    position = models.CharField('Должность', max_length=255, null=True, blank=True)
    photo = models.ImageField('Фото', upload_to='team', null=True, blank=True)
    text = models.CharField('Текст', max_length=1024, null=True, blank=True)
    email = models.EmailField('E-Mail', max_length=255, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=255, null=True, blank=True)
    is_visible = models.BooleanField('Включено', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
