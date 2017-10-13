from django.test import TestCase
from news.models import News
from django.core.exceptions import ValidationError


class NewsModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_news = News()
        first_news.title = 'Новость 1'
        first_news.text = 'Текст новости 1'
        first_news.save()

        second_news = News()
        second_news.title = 'Новость 2'
        second_news.text = 'Текст новости 2'
        second_news.save()

        saved_first_news = News.objects.first()
        self.assertEqual(first_news, saved_first_news)

        saved_news = News.objects.all()
        self.assertEqual(saved_news.count(), 2)

        first_saved_news = saved_news[0]
        second_saved_news = saved_news[1]
        self.assertEqual(first_saved_news.title, 'Новость 1')
        self.assertEqual(first_saved_news.text, 'Текст новости 1')
        self.assertEqual(second_saved_news.title, 'Новость 2')
        self.assertEqual(second_saved_news.text, 'Текст новости 2')

    def test_cannot_save_empty_news(self):
        news = News()
        news.save()
        with self.assertRaises(ValidationError):
            news.save()
            news.full_clean()
