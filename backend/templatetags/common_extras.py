from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from apps.settings.models import Analytics

register = template.Library()


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.inclusion_tag('_partial/widgets/comments.html', takes_context=True)
def comments_widget(context, identifier, identifier_id):
    """Виджет комментариев Disqus."""
    return {
        'is_secure': context['request'].is_secure(),
        'host': context['request'].get_host(),
        'full_path': context['request'].get_full_path(),
        'identifier': identifier,
        'identifier_id': identifier_id
    }


@register.simple_tag
def analytics_code():
    """Возвращает HTML-код аналитики."""
    analytics, created = Analytics.objects.get_or_create()
    return mark_safe(analytics.code)


@register.filter(is_safe=False)
@stringfilter
def pluralize(value, forms):
    """
    Подбирает окончание существительному после числа
    {{someval|pluralize:"товар,товара,товаров"}}
    """
    try:
        one, two, many = forms.split(u',')
        value = str(value)[-2:]  # 314 -> 14

        if 21 > int(value) > 4:
            return many

        if value.endswith('1'):
            return one
        elif value.endswith(('2', '3', '4')):
            return two
        else:
            return many

    except (ValueError, TypeError):
        return ''
