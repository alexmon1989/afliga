from django import template
from apps.settings.models import FooterSettings, Banner

register = template.Library()


@register.inclusion_tag('_partial/footer.html')
def my_footer():
    return {'footer_data': FooterSettings.objects.first()}


@register.simple_tag
def banner(pk):
    banner_item = Banner.objects.filter(pk=pk, is_visible=True).first()
    return banner_item
