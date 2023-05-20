from unittest import TestCase
from datetime import datetime

from module_03_ci_culture_beginning.homework.hw3.accounting import app


class TestAccounting(TestCase):
    storage = dict()

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url_add = '/add/'
        cls.base_url_calculate = '/calculate/'
        cls.storage = {
                        2021: {
                            1: 50,
                            2: 100,
                            10: 500
                        },
                        2022: {
                            3: 10,
                            7: 75,
                            12: 1000
                        },
                        2023: {1: 200}
                       }

    def test_can_add_expense_value(self):
        today_date = datetime.today()
        year = str(today_date.year)
        today_str = today_date.strftime('%Y%m%d')
        expense = '1'

        response = self.app.get(self.base_url_calculate + year)
        response_text_list = response.data.decode().split()
        first_value = response_text_list[4]

        self.__add_expense(today_str, expense)

        response = self.app.get(self.base_url_calculate + year)
        response_text_list = response.data.decode().split()
        second_value = response_text_list[4]

        difference = int(second_value) - int(first_value)
        self.assertEqual(int(expense), difference)

    def test_can_get_error_if_try_to_add_wrong_expense(self):
        date_str = datetime.today().strftime('%Y%m%d')
        expense = 'test'

        response = self.__add_expense(date_str, expense)
        self.assertTrue(response.status_code == 404)

    def test_can_get_error_if_try_to_add_wrong_date(self):
        date_str = '20230000'
        expense = '50'

        with self.assertRaises(ValueError):
            self.__add_expense(date_str, expense)

    def test_can_get_expense_of_year(self):
        year = 2021
        self.__add_expense_from_storage(year)

        response = self.app.get(self.base_url_calculate + str(year))
        response_text_list = response.data.decode().split()
        expense_from_response = int(response_text_list[4])
        expense_from_storage = 0

        for month, expense in self.storage[year].items():
            expense_from_storage += expense

        self.assertEqual(expense_from_response, expense_from_storage)

    def test_can_get_error_for_wrong_year(self):
        year = 'test'
        response = self.app.get(self.base_url_calculate + year)
        self.assertTrue(response.status_code == 404)

    def test_can_get_error_for_nonexistent_year(self):
        year = 10000

        with self.assertRaises(ValueError):
            self.app.get(self.base_url_calculate + str(year))

    def test_can_get_zero_expense_for_nonexistent_record_of_year(self):
        year = 2020
        response = self.app.get(self.base_url_calculate + str(year))
        response_text_list = response.data.decode().split()
        expense_from_response = int(response_text_list[4])

        self.assertTrue(expense_from_response == 0)

    def test_can_get_expense_of_month(self):
        year = 2022
        month = 7

        self.__add_expense_from_storage(year)

        url = self.base_url_calculate + str(year) + '/' + str(month)
        response = self.app.get(url)
        response_text_list = response.data.decode().split()
        expense_from_response = int(response_text_list[3])

        expense_from_storage = self.storage[year][month]

        self.assertEqual(expense_from_response, expense_from_storage)

    def test_can_get_error_for_wrong_year_from_calculate_month(self):
        year = 10000

        with self.assertRaises(ValueError):
            url = self.base_url_calculate + str(year) + '/01'
            self.app.get(url)

    def test_can_get_error_for_wrong_month_from_calculate_month(self):
        year = 2023
        month = 15

        with self.assertRaises(ValueError):
            url = self.base_url_calculate + str(year) + '/' + str(month)
            self.app.get(url)

    def test_can_get_zero_expense_for_nonexistent_record_of_date(self):
        year = 2020
        month = 1

        response = self.app.get(self.base_url_calculate + str(year) + '/' + str(month))
        response_text_list = response.data.decode().split()
        expense_from_response = int(response_text_list[3])

        self.assertTrue(expense_from_response == 0)

    def __add_expense(self, date: str, expense: str) -> object:
        return self.app.get(self.base_url_add + date + '/' + expense)

    def __add_expense_from_storage(self, year: int) -> None:

        for month, expense in self.storage[year].items():

            if month < 10:
                month_str = '0' + str(month)
            else:
                month_str = str(month)

            date_str = ''.join((str(year), month_str, '01'))
            self.__add_expense(date_str, str(expense))






