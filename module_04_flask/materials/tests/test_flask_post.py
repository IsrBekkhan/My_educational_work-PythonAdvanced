from unittest import TestCase
import json

from requests_toolbelt.multipart.encoder import MultipartEncoder

from module_04_flask.materials.flask_post import app


class TestSum(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/sum'

    def test_can_get_numbers_sum(self):
        data = {'array1': [1, 2, 3],
                'array2': [1, 1, 1]}
        result = ','.join(str(a1 + a2) for (a1, a2) in zip(data['array1'], data['array2']))

        response = self.app.post(self.base_url, data=data)
        response_text = response.data.decode()
        self.assertTrue(result in response_text)


class TestSum2(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/sum2'

    def test_can_get_numbers_sum(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'array1': '1,2,3',
                'array2': '1,1,1'}
        result = ','.join(
            str(int(a1) + int(a2)) for (a1, a2) in zip(data['array1'].split(','), data['array2'].split(','))
        )
        response = self.app.post(self.base_url, headers=headers, data=data)
        response_text = response.data.decode()
        self.assertTrue(result in response_text)


class TestSum3(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/sum3'

    def test_can_get_numbers_sum(self):
        data = {'array1': [1, 2, 3],
                'array2': [1, 1, 1]}
        result = ','.join(str(a1 + a2) for (a1, a2) in zip(data['array1'], data['array2']))
        response = self.app.post(self.base_url, data=json.dumps(data))
        response_text = response.data.decode()
        self.assertTrue(result in response_text)
