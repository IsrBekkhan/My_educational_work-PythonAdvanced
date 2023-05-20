import unittest

from module_03_ci_culture_beginning.materials.testing_age.social_age import get_social_status


class TestSocialAge(unittest.TestCase):

    def test_can_get_child_age(self):
        age = 8
        expected_res = 'ребенок'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_teenager_age(self):
        age = 15
        expected_res = 'подросток'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_adult_age(self):
        age = 20
        expected_res = 'взрослый'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_elderly_age(self):
        age = 50
        expected_res = 'пожилой'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_pensioner_age(self):
        age = 65
        expected_res = 'пенсионер'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_negative_age(self):
        age = -8
        with self.assertRaises(ValueError):
            get_social_status(age)

    def test_cannot_pass_str_as_age(self):
        age = 'old'
        with self.assertRaises(ValueError):
            get_social_status(age)

    def test_can_get_wrong_age_type(self):
        age = dict()
        with self.assertRaises(ValueError):
            get_social_status(age)

