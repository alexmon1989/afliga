from django.db import models


class ContactEmail(models.Model):
    """Модель E-Mail, на который отправляются данные формы контактов."""
    email = models.EmailField('E-Mail')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "E-Mail формы контактов"
        verbose_name_plural = "E-Mail формы контактов"


class Contact(models.Model):
    """Модель данных страницы контактов."""
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Текст', max_length=1024)
    phones = models.TextField('Телефон(ы)', max_length=255)
    emails = models.TextField('E-Mail(ы)', max_length=255)

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"
