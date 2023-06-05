import unittest

from decrypt import decrypt


class TestDecrypt(unittest.TestCase):

    def test_can_get_decrypted_message(self) -> None:
        decrypt_dict = {'абра-кадабра.': 'абра-кадабра',
                        'абраа..-кадабра': 'абра-кадабра',
                        'абраа..-.кадабра': 'абра-кадабра',
                        'абра--..кадабра': 'абра-кадабра',
                        'абрау...-кадабра': 'абра-кадабра',
                        'абра........': '',
                        'абр......a.': 'a',
                        '1..2.3': '23',
                        '.': '',
                        '1.......................': ''}

        for key, value in decrypt_dict.items():

            with self.subTest(f'Тест строки {key}', n=key):
                self.assertEqual(decrypt(key), value)
