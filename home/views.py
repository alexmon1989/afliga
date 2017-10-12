from django.shortcuts import render


def home_page(request):
    """Отображает главную страницу."""
    return render(request, 'home/home.html')
