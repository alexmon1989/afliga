from .base import FunctionalTest


class NewsTest(FunctionalTest):
    """Тест наличия блоков на главной странице."""

    fixtures = ['news.json']

    def test_news_list_exists(self):
        # Пользователь заходит на страницу новостей
        self.browser.get(self.live_server_url + '/news/')

        # Видит, что title и h1 соответствуют этой странице
        self.assertIn('Новости', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Новости', header_text)

        # Видит список новостей
        news_list = self.browser.find_element_by_class_name('news_list')
        self.assertIsNotNone(news_list)

    def test_news_list_contains_news(self):
        # Пользователь заходит на страницу новостей
        self.browser.get(self.live_server_url + '/news/')

        # Видит, что среди новостей есть новость с заголовком "Новость 1" и текстом "Текст новости 1"
        news_list = self.browser.find_element_by_class_name('news_list')
        news_titles = news_list.find_elements_by_class_name('title')
        self.assertIn('Новость 1', [title.text for title in news_titles])
        news_titles = news_list.find_elements_by_class_name('text')
        self.assertIn('Текст новости 1', [title.text for title in news_titles])
