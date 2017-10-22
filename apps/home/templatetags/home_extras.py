from django import template
from apps.settings.models import FooterSettings

register = template.Library()


@register.inclusion_tag('_partial/footer.html')
def my_footer():
    return {'footer_data': FooterSettings.objects.first()}
