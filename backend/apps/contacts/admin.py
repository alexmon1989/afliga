from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.contacts.models import Contact, ContactEmail

admin.site.register(Contact, SingleModelAdmin)


@admin.register(ContactEmail)
class ContactEmailsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования Email, на которые отправляются данные формы контактов."""
    ordering = ('email',)
    search_fields = ('email',)
