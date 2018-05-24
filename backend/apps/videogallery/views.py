from django.views.generic import ListView
from apps.videogallery.models import Video


class VideosListView(ListView):
    """Отображает страницу со списком видеозаписей."""
    model = Video
    template_name = 'videogallery/list.html'
    paginate_by = 12

    def get_queryset(self):
        return Video.objects.filter(is_visible=True).order_by('-created_at')
