import unittest
from remote_execution import app


class TestRunCode(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/run_code'
        self.base_headers = {
            'Content-Type':
            'application/x-www-form-urlencoded'
        }

    def test_can_get_timeout_error(self):
        code_timeout = {'code': 'import time\ntime.sleep(11)',
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('Превышено' in response.text)

    def test_can_get_unsecure_code_error(self):
        code_timeout = {'code': "from subprocess import run\nrun(['./kill_the_system.sh'])",
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('BlockingIOError' in response.text)

    def test_can_get_syntax_error(self):
        code_timeout = {'code': "print('OK'",
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('NameError' or 'SyntaxError' in response.text)

    def test_can_get_name_error(self):
        code_timeout = {'code': "pritn('OK')",
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('NameError' in response.text)

    def test_can_get_right_result(self):
        code_timeout = {'code': "print('Hello world')",
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 200)

        with self.subTest():
            self.assertTrue('Hello world' in response.text)

    def test_can_get_empty_code_error(self):
        code_timeout = {'code': "",
                        'timeout': 10}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('code' in response.text)

    def test_can_get_to_high_timeout_error(self):
        code_timeout = {'code': "print('Hello world')",
                        'timeout': 31}
        response = self.app.post(self.base_url, headers=self.base_headers, data=code_timeout)

        with self.subTest():
            self.assertTrue(response.status_code == 400)

        with self.subTest():
            self.assertTrue('timeout' in response.text)


if __name__ == '__main__':
    unittest.main()
