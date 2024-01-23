import aiohttp
import requests

import asyncio

from models import Coffee, User
from database import session


NAMES_LIST = [
        'Вероника', 'Алиса', 'Григорий', 'Александр', 'Артём',
        'Таисия', 'Николай', 'Тимофей', 'Роман', 'Владимир'
    ]


def get_address():
    response = requests.get('https://random-data-api.com/api/address/random_address')
    return response.json()


async def random_coffee(client: aiohttp.ClientSession) -> Coffee:
    async with client.get('https://random-data-api.com/api/coffee/random_coffee') as response:
        if response.status == 200:
            coffee_json = await response.json()
            return Coffee(
                title=coffee_json['blend_name'],
                origin=coffee_json['origin'],
                intensifier=coffee_json['intensifier'],
                notes=coffee_json['notes'].split(', ')
            )


async def random_user(client: aiohttp.ClientSession, coffee_id: int, user_name: str) -> User:
    async with client.get('https://random-data-api.com/api/address/random_address') as response:
        if response.status == 200:
            address_json = await response.json()
            return User(
                name=user_name,
                address=address_json,
                coffee_id=coffee_id
            )


async def get_coffee_list(count: int):

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5)) as client:
        tasks = [random_coffee(client) for _ in range(count)]
        return await asyncio.gather(*tasks)


async def get_user_list(count: int):

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5)) as client:
        tasks = [
            random_user(client, coffee_id=num + 1, user_name=NAMES_LIST[num]) for num in range(count)
        ]
        return await asyncio.gather(*tasks)


def create_random_data(count: int):
    coffee_list = asyncio.run(get_coffee_list(count))
    users_list = asyncio.run(get_user_list(count))

    session.bulk_save_objects(coffee_list)
    session.bulk_save_objects(users_list)
    session.commit()



