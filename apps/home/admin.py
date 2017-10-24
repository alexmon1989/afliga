from django.contrib import admin
from apps.home.models import Carousel


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования слайдера."""
    list_display = ('title', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)
