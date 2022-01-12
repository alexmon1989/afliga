from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.league.models import Season, Group, Team
import json


@receiver(post_save, sender=Season, dispatch_uid="save_season")
def update_season_is_current_season(sender, instance, **kwargs):
    """Обработчик сигнала сохранения модели Season. Цель - всегда иметь только один 'текущий сезон'."""
    if instance.is_current_season:
        Season.objects.exclude(pk=instance.pk).update(is_current_season=False)


@receiver(m2m_changed, sender=Group.teams.through)
def group_save_callback(sender, instance, action, reverse, model, pk_set, *args, **kwargs):
    """Обработчик сигнала изменения поля teams модели Group. Меняет содержимое поля table."""
    data = json.loads(instance.table or '[]')
    if action == 'pre_remove':
        new_data = [x for x in data if x['id'] not in pk_set]
        instance.table = json.dumps(new_data)
        instance.save()
    if action == 'pre_add':
        for pk in pk_set:
            data.append({
                'id': pk,
                'title': Team.objects.filter(pk=pk).first().title,
                'games': 0,
                'wins': 0,
                'draws': 0,
                'defeats': 0,
                'goals_scored': 0,
                'goals_missed': 0,
                'score': 0,
            })
        instance.table = json.dumps(data)
        instance.save()
