from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.settings.models import FooterSettings

admin.site.register(FooterSettings, SingleModelAdmin)
