from django import template
from apps.settings.models import FooterSettings, Banner, PersonWidget

register = template.Library()


@register.inclusion_tag('_partial/footer.html')
def my_footer():
    return {'footer_data': FooterSettings.objects.first()}


@register.inclusion_tag('_partial/widgets/person.html')
def person_widget():
    return {'person_widget_data': PersonWidget.objects.first()}


@register.simple_tag
def banner(pk):
    banner_item = Banner.objects.filter(pk=pk, is_visible=True).first()
    return banner_item


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')
