from django.contrib import admin
from apps.team.models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Класс для описания интерфейса администрирования новостей."""
    list_display = ('name', 'position', 'email', 'phone', 'is_visible', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('is_visible',)
    search_fields = ('name', 'position', 'email', 'phone')
