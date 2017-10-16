from django.test import TestCase
from news.models import News


class ListPageTest(TestCase):

    def test_list_page_returns_correct_html(self):
        response = self.client.get('/news/')
        self.assertTemplateUsed(response, 'news/list.html')

    def test_displays_news(self):
        news_1 = News()
        news_1.title = 'Новость 1'
        news_1.text = 'Текст новости 1'
        news_1.save()

        news_2 = News()
        news_2.title = 'Новость 2'
        news_2.text = 'Текст новости 2'
        news_2.save()

        response = self.client.get('/news/')
        self.assertContains(response, 'Новость 1')
        self.assertContains(response, 'Текст новости 1')
        self.assertContains(response, 'Новость 2')
        self.assertContains(response, 'Текст новости 2')
