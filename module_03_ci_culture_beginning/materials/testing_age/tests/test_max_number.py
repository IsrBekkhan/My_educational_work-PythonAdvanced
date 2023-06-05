import unittest
from os import remove


from module_03_ci_culture_beginning.materials.testing_age.max_number_app import app


class TestMaxNumberApp(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/max_number/'
        self.test_file = 'test_file.txt'

        with open(self.test_file, 'w') as test_file:
            test_file.write('test')

    def test_can_get_correct_max_number_in_series_of_two(self):
        numbers_ = 1, 2
        url = self.base_url + '/'.join(str(number) for number in numbers_)
        response = self.app.get(url)
        response_text = response.data.decode()
        correct_answer_str = f'{max(numbers_)}'
        self.assertTrue(correct_answer_str in response_text)

    def test_can_get_error_for_wrong_value(self):
        numbers_ = 'f', 2
        url = self.base_url + '/'.join(str(number) for number in numbers_)
        response = self.app.get(url)
        response_text = response.data.decode()
        correct_answer_str = 'Ошибка'
        self.assertTrue(correct_answer_str in response_text)

    def tearDown(self) -> None:
        remove(self.test_file)




