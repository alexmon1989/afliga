from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from apps.news.models import News
from apps.photogallery.models import Gallery
from apps.league.models import Tournament, Team, Player, Match


class StaticSitemap(Sitemap):
    def items(self):
        return [
            'home',
            'contacts',
            'videos_list',
            'team_list',
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    def items(self):
        return News.objects.filter(is_visible=True)

    def lastmod(self, obj):
        return obj.updated_at


class GallerySitemap(Sitemap):
    def items(self):
        return Gallery.objects.filter(is_visible=True)

    def lastmod(self, obj):
        return obj.updated_at


class TournamentSitemap(Sitemap):
    def items(self):
        return Tournament.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class TeamSitemap(Sitemap):
    def items(self):
        return Team.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class PlayerSitemap(Sitemap):
    def items(self):
        return Player.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class MatchSitemap(Sitemap):
    def items(self):
        return Match.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
