from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from apps.contacts.models import Contact

admin.site.register(Contact, SingleModelAdmin)
