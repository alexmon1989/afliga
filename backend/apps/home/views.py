from django.shortcuts import render
from django.views.decorators.cache import cache_page
from apps.home.models import Carousel, LastCompetition
from apps.news.models import News
from apps.videogallery.models import Video


@cache_page(None)
def home_page(request):
    """Отображает главную страницу."""
    last_news = News.objects.filter(is_visible=True).order_by('-created_at').all()[:4]
    last_videos = Video.objects.filter(is_visible=True).order_by('-created_at').all()[:3]
    slides = Carousel.objects.filter(is_visible=True).order_by('-created_at').all()
    tournaments = LastCompetition.objects.order_by('-created_at').all()

    return render(request, 'home/home.html', {
        'last_news': last_news,
        'last_videos': last_videos,
        'slides': slides,
        'tournaments': tournaments,
    })
