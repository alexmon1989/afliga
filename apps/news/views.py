from django.views.generic import ListView
from apps.news.models import News


class NewsList(ListView):
    """Отображает страницу со списком новостей."""
    model = News
    template_name = 'news/list.html'
