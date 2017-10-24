from django.contrib import admin
from apps.videogallery.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования галерей."""
    list_display = ('title', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)
