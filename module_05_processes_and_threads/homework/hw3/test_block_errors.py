import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):

    def test_can_get_error(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_can_ignore_error(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except:
            self.fail()

    def test_can_ignore_inner_error(self):
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    a = 1 / '0'
        except:
            self.fail()

    def test_can_ignore_subclass_error(self):
        try:
            with BlockErrors({Exception}):
                a = 1 / '0'
        except:
            self.fail()

    def test_can_get_type_error(self):
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / '0'


if __name__ == '__main__':
    unittest.main()
