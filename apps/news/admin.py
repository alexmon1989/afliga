from django.contrib import admin
from apps.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования новостей."""
    list_display = ('title', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)
