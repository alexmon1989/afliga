from django.contrib import admin
from apps.photogallery.models import Gallery, Photo


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования галерей."""
    list_display = ('title', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования фотографий."""
    list_filter = ('gallery', 'is_visible')
    list_display = ('id', 'gallery', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('gallery',)
