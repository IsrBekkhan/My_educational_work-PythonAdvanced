import json

import requests

import logging

logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://0.0.0.0:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))


if __name__ == '__main__':
    client = BookClient()
    client.session.post(
        client.URL,
        data=json.dumps({'title': '123', 'author': 'name'}),
        headers={'content-type': 'application/json'}
    )
