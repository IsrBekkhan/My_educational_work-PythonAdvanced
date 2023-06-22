import unittest
from redirect import Redirect

from os import path, remove


class TestRedirect(unittest.TestCase):

    def setUp(self) -> None:
        self.output_file = 'output_test.txt'
        self.errors_file = 'errors_test.txt'

        self.output_test = open(self.output_file, 'w')
        self.errors_test = open(self.errors_file, 'w')

        self.stdout_message = 'Hello world!'
        self.stderr_message = "It's test exception"

    def test_can_correct_work(self):

        with Redirect(stdout=self.output_test, stderr=self.errors_test):
            print(self.stdout_message)
            raise Exception(self.stderr_message)

        if path.exists(self.output_file):

            with open(self.output_file, 'r') as output_file:
                output_text = output_file.read()

                with self.subTest():
                    self.assertTrue(self.stdout_message in output_text)

        if path.exists(self.errors_file):

            with open(self.errors_file, 'r') as errors_file:
                errors_text = errors_file.read()

                with self.subTest():
                    self.assertTrue(self.stderr_message in errors_text)

    def tearDown(self) -> None:

        if path.exists(self.output_file):
            remove(self.output_file)

        if path.exists(self.errors_file):
            remove(self.errors_file)


if __name__ == '__main__':
    unittest.main()

    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)

