import unittest

from datetime import datetime

from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(unittest.TestCase):

    def setUp(self) -> None:
        self.person = Person(name='Имя', year_of_birth=1990, address='Город')

    def test_can_get_age(self):
        year_now = datetime.now().year
        age = year_now - self.person.yob
        self.assertEqual(age, self.person.get_age())

    def test_can_get_name(self):
        name = self.person.name
        self.assertEqual(name, self.person.get_name())

    def test_can_set_name(self):
        name = 'Бекхан'
        self.person.set_name(name=name)
        self.assertEqual(name, self.person.name)

    def test_can_set_address(self):
        address = 'Грозный'
        self.person.set_address(address=address)
        self.assertEqual(address, self.person.address)

    def test_can_get_address(self):
        address = 'Грозный'
        self.person.address = address
        self.assertEqual(address, self.person.get_address())

    def test_can_check_is_homeless(self):
        is_homeless = self.person.address is None
        self.assertEqual(is_homeless, self.person.is_homeless())

