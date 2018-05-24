from django.views.generic import ListView, DetailView
from apps.news.models import News


class NewsListView(ListView):
    """Отображает страницу со списком новостей."""
    model = News
    template_name = 'news/list.html'
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(is_visible=True).order_by('-created_at')


class NewsDetailView(DetailView):
    """Отображает страницу с новостью."""
    model = News
    template_name = 'news/detail.html'
    queryset = News.objects.filter(is_visible=True)

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['more_news'] = self.queryset.order_by('-created_at').exclude(pk=self.kwargs['pk'])[:3]
        return context