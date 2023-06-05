"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistration(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'
        self.base_headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }
        self.base_data = {
            'email': 'israpal@bk.ru',
            'phone': '9280002425',
            'name': 'Исрапилов Б.Х.',
            'address': 'г. Урус-Мартан',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }

    def test_can_handle_right_request(self):
        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        self.assertTrue(response.status_code == 200)

    def test_can_error_for_empty_fields(self):

        for key, value in self.base_data.items():
            self.base_data[key] = ''

        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)

        for key, value in self.base_data.items():

            with self.subTest(key):
                self.assertTrue(key in response_text)

    def test_can_get_error_for_incorrect_email(self):
        self.base_data['email'] = 'israpalbk.ru'
        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('email' in response_text)

    def test_can_get_error_for_incorrect_phone(self):
        self.base_data['phone'] = '89280002425'
        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('phone' in response_text)

    def test_can_get_error_for_letter_in_phone(self):
        self.base_data['phone'] = '928000242L'
        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('phone' in response_text)

    def test_can_get_error_for_letter_in_index(self):
        self.base_data['index'] = '36650T'
        response = self.app.post(self.base_url, headers=self.base_headers, data=self.base_data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('index' in response_text)

    def tearDown(self) -> None:
        self.base_data = {
            'email': 'israpal@bk.ru',
            'phone': '9280002425',
            'name': 'Исрапилов Б.Х.',
            'address': 'г. Урус-Мартан',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }


if __name__ == '__main__':
    unittest.main()
