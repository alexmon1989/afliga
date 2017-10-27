"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from apps.home import views as home_views
from apps.news import urls as news_urls
from apps.contacts import urls as contacts_urls
from apps.team import urls as team_urls
from apps.photogallery import urls as photogallery_urls
from apps.videogallery import urls as videogallery_urls
from apps.league import urls as league_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_views.home_page, name='home'),
    url(r'^news/', include(news_urls)),
    url(r'^contacts/', include(contacts_urls)),
    url(r'^team/', include(team_urls)),
    url(r'^photo-gallery/', include(photogallery_urls)),
    url(r'^video/', include(videogallery_urls)),
    url(r'^league/', include(league_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
