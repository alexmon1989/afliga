from django.contrib import admin
from apps.home.models import Carousel, LastCompetition, WidgetsSettings


@admin.register(WidgetsSettings)
class WidgetsSettingsAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования виджетов главной страницы."""
    list_display = (
        'competition', 'show_table', 'show_bombardiers', 'show_penalties', 'show_assistants', 'created_at', 'updated_at'
    )
    ordering = ('-created_at',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования слайдера."""
    list_display = ('title', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)


@admin.register(LastCompetition)
class LastCompetitionAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования слайдера."""
    list_display = ('id', 'competition', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('competition',)
