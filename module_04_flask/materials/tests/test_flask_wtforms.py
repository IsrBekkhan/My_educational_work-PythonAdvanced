from unittest import TestCase

from module_04_flask.materials.flask_wtform import app


class TestRegistration(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_can_get_error_for_empty_email(self):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }
        data = {
            'email': '',
            'phone': '9280002425',
            'name': 'Исрапилов Б.Х.',
            'address': 'г. Урус-Мартан',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }
        response = self.app.post(self.base_url, headers=headers, data=data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('email' in response_text)

    def test_can_get_error_for_empty_phone(self):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }
        data = {
            'email': 'israpal@bk.ru',
            'phone': '10000000000',
            'name': 'Исрапилов Б.Х.',
            'address': 'г. Урус-Мартан',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }
        response = self.app.post(self.base_url, headers=headers, data=data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('phone' in response_text)

    def test_can_get_error_for_empty_name(self):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }
        data = {
            'email': 'israpal@bk.ru',
            'phone': '9280002425',
            'name': 'Исрапилов Бекхан',
            'address': 'г. Урус-Мартан',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }
        response = self.app.post(self.base_url, headers=headers, data=data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('name' in response_text)

    def test_can_get_error_for_empty_address(self):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }
        data = {
            'email': 'israpal@bk.ru',
            'phone': '9280002425',
            'name': 'Исрапилов Б.Х.',
            'address': '',
            'index': '366500',
            'comment': 'глвные дороги загружены'
        }
        response = self.app.post(self.base_url, headers=headers, data=data)
        response_text = response.data.decode()
        self.assertTrue(response.status_code == 400)
        self.assertTrue('address' in response_text)

