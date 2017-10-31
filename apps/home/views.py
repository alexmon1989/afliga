from django.shortcuts import render
from apps.home.models import Carousel, LastTournament
from apps.news.models import News
from apps.videogallery.models import Video


def home_page(request):
    """Отображает главную страницу."""
    last_news = News.objects.filter(is_visible=True).order_by('-created_at').all()[:4]
    last_videos = Video.objects.filter(is_visible=True).order_by('-created_at').all()[:3]
    slides = Carousel.objects.filter(is_visible=True).order_by('-created_at').all()
    tournaments = LastTournament.objects.order_by('-created_at').all()

    return render(request, 'home/home.html', {
        'last_news': last_news,
        'last_videos': last_videos,
        'slides': slides,
        'tournaments': tournaments,
    })
