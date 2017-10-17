from django.shortcuts import render
from apps.news.models import News


def home_page(request):
    """Отображает главную страницу."""
    return render(request, 'home/home.html', {
        'last_news': News.objects.filter(is_visible=True).order_by('-created_at')[:4]
    })
