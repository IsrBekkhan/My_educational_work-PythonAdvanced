import requests


def get_content_len(url: str):
    response = requests.get(url, timeout=(5, 5))
    return len(response.content)


def mult_numbers(number: int):
    return sum(i * i for i in range(number))
