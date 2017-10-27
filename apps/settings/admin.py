from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.settings.models import FooterSettings, Banner, PersonWidget

admin.site.register(FooterSettings, SingleModelAdmin)
admin.site.register(PersonWidget, SingleModelAdmin)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования баннеров."""
    list_display = ('title', 'is_visible', 'link', 'updated_at')
    ordering = ('created_at',)
    list_editable = ('is_visible',)
    search_fields = ('title',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
