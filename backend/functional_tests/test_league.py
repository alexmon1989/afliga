from .base import FunctionalTest
from model_bakery import baker


class LeagueTest(FunctionalTest):
    def test_match_contains_history(self):
        # Пользователь заходит на страницу соревнований
        self.browser.get(self.live_server_url + '/league/')

        # Видит, что среди соревнований есть соревнование "Соревнование 1" и "Соревнование 2"
        competitions_list = self.browser.find_element_by_css_selector('news_list')
        competitions_titles = competitions_list.find_elements_by_css_selector('li')
        competitions_titles_texts = [title.text for title in competitions_titles]
        self.assertIn('Соревнование 1', competitions_titles_texts)
        self.assertIn('Соревнование 2', competitions_titles_texts)
