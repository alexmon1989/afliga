from django import template
from apps.home.models import WidgetsSettings
from apps.settings.models import FooterSettings, Banner, PersonWidget

register = template.Library()


@register.inclusion_tag('_partial/footer.html')
def my_footer():
    return {'footer_data': FooterSettings.objects.first()}


@register.inclusion_tag('_partial/widgets/person.html')
def person_widget():
    return {'person_widget_data': PersonWidget.objects.first()}


@register.inclusion_tag('_partial/widgets/bombardiers.html')
def bombardiers_widget():
    return {'competitions': WidgetsSettings.objects.filter(show_bombardiers=True).order_by('-created_at').all()}


@register.inclusion_tag('_partial/widgets/assistants.html')
def assistants_widget():
    return {'competitions': WidgetsSettings.objects.filter(show_assistants=True).order_by('-created_at').all()}


@register.inclusion_tag('_partial/widgets/penalties.html')
def penalties_widget():
    return {'competitions': WidgetsSettings.objects.filter(show_penalties=True).order_by('-created_at').all()}


@register.inclusion_tag('_partial/widgets/table.html')
def table_widget():
    return {'tables': WidgetsSettings.objects.filter(show_table=True).order_by('-created_at').all()}


@register.inclusion_tag('home/_partial/matches.html')
def matches_block(competition):
    return {'competition': competition.competition}


@register.simple_tag
def banner(pk):
    banner_item = Banner.objects.filter(pk=pk, is_visible=True).first()
    return banner_item
