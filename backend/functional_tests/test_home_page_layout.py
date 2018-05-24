from .base import FunctionalTest


class LayoutTest(FunctionalTest):
    """Тест наличия блоков на главной странице."""

    def test_layout(self):
        # Пользователь заходит на главную
        self.browser.get(self.live_server_url)

        # Видит наличие изображения с логотипом
        logo_img = self.browser.find_element_by_id('logo_img')
        self.assertIsNotNone(logo_img)

        # Видит наличие меню и элементов в нём
        top_menu = self.browser.find_element_by_id('top_menu')
        self.assertIsNotNone(top_menu)
        top_menu_html = top_menu.get_attribute('innerHTML')
        self.assertInHTML('Главная', top_menu_html)
        self.assertInHTML('Новости', top_menu_html)
        self.assertInHTML('Медиа', top_menu_html)
        self.assertInHTML('Руководство', top_menu_html)
        self.assertInHTML('Турниры', top_menu_html)
        self.assertInHTML('Контакты', top_menu_html)

        # Видит наличие слайдера.
        slider = self.browser.find_element_by_id('slider')
        self.assertIsNotNone(slider)

        # Видит наличие блока последних новостей
        latest_news = self.browser.find_element_by_id('latest_news')
        self.assertIsNotNone(latest_news)

        # Видит наличие 4 рекламных баннеров
        for i in range(1, 4):
            banner = self.browser.find_element_by_id('banner_{}'.format(i))
            self.assertIsNotNone(banner)

        # Видит данные матчей последнего турнира
        matches_latest_tournament = self.browser.find_element_by_id('matches_latest_tournament')
        self.assertIsNotNone(matches_latest_tournament)

        # Видит данные матчей предпоследнего турнира
        matches_prelatest_tournament = self.browser.find_element_by_id('matches_prelatest_tournament')
        self.assertIsNotNone(matches_prelatest_tournament)

        # Видит видео-галерею
        video_gallery = self.browser.find_element_by_id('video_gallery')
        self.assertIsNotNone(video_gallery)

        # И кнопку перехода на страницу со всеми видео
        all_videos_btn = video_gallery.find_element_by_class_name('btn')
        self.assertEqual(all_videos_btn.text, 'Все видеозаписи')

        # Смотрит, что на странице есть блок виджетов:
        widgets = self.browser.find_element_by_class_name('widgets')
        # А в нём следующие виджеты:
        # Турнирная таблица
        table = widgets.find_element_by_id('tournament_table')
        self.assertIsNotNone(table)
        # Бомбардиры
        bombardiers = widgets.find_element_by_id('bombardiers')
        self.assertIsNotNone(bombardiers)
        # Штрафники
        penalties = widgets.find_element_by_id('penalties')
        self.assertIsNotNone(penalties)
        # Персона
        person = widgets.find_element_by_id('person')
        self.assertIsNotNone(person)

        # Смотрит, что на странице есть футер
        footer = self.browser.find_element_by_tag_name('footer')
        footer_html = footer.get_attribute('innerHTML')
        # И такие блоки в нём:
        # Навигация
        self.assertInHTML('Навигация', footer_html)
        # Информация
        self.assertInHTML('Информация', footer_html)
        # Контактная информация
        self.assertInHTML('Контактная информация', footer_html)
        # Ссылки на соц. сети
        self.assertIsNotNone(footer.find_element_by_id('fb_link'))
        self.assertIsNotNone(footer.find_element_by_id('vk_link'))
        self.assertIsNotNone(footer.find_element_by_id('twitter_link'))
        self.assertIsNotNone(footer.find_element_by_id('google_link'))
        # Копирайт
        self.assertIsNotNone(footer.find_element_by_id('copyrights'))
