from django.conf.urls import url
from apps.team.views import TeamListView

urlpatterns = [
    url(r'^$', TeamListView.as_view(), name='team_list'),
]
