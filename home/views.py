from django.shortcuts import render


def home_page(request):
    """Отображает главную страницу."""
    from news.models import News
    news = News()
    news.save()
    return render(request, 'home/home.html')
