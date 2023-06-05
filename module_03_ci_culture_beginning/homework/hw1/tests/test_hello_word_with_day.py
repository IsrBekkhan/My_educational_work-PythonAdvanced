from freezegun import freeze_time

import unittest
from datetime import datetime

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app, GREETINGS


class TestHelloWordWithDay(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'
        self.username = 'username'

    @freeze_time('2023-05-8')
    def test_can_get_correct_monday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-9')
    def test_can_get_correct_tuesday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-10')
    def test_can_get_correct_wednesday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-11')
    def test_can_get_correct_thursday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-12')
    def test_can_get_correct_friday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-13')
    def test_can_get_correct_saturday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    @freeze_time('2023-05-13')
    def test_can_get_correct_sunday(self):
        weeks_day_index = datetime.today().weekday()
        weeks_day = GREETINGS[weeks_day_index]
        response = self.app.get(self.base_url + self.username)
        response_text = response.data.decode()
        self.assertTrue(weeks_day in response_text)

    def test_is_username_like_weeks_day(self):

        for hello_message in GREETINGS:
            self.assertNotEqual(hello_message, self.username)


