import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from asyncio.exceptions import TimeoutError
import aiofiles
from bs4 import BeautifulSoup

from typing import List


# URL = ['https://a-parser.com/']
URL = ['https://skillbox.ru/']


async def get_urls(session: aiohttp.ClientSession, url: str, iter_count: int):
    try:
        async with session.get(url) as response:
            text = await response.text()
            all_links = await asyncio.to_thread(html_parse, text)
            external_links = get_external_links(all_links, url)[:iter_count]
            print(external_links)
            await write_to_disk(external_links)
            return external_links
    except (ClientConnectorError, ConnectionResetError, TimeoutError):
        pass


def html_parse(html_text: str) -> List[str]:
    soup = BeautifulSoup(html_text, 'html.parser')
    return [link.get('href') for link in soup.find_all('a')]


def get_external_links(links: List[str], url: str) -> List[str]:
    external_links = []

    for link in links:
        if link:
            if url not in link and link.startswith('http'):
                external_links.append(link)

    return external_links


async def write_to_disk(external_links: List[str]):
    async with aiofiles.open('crawler_result.txt', mode='a') as text_file:
        await text_file.write('\n'.join(external_links))


async def web_crawler(urls: List[str], iter_count: int = 3):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(5)) as session:
        tasks = [get_urls(session, url, iter_count) for url in urls]
        result = await asyncio.gather(*tasks)
        await web_crawler(result[0])


if __name__ == '__main__':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Для запуска кода на Windows
    # Обуждение вопроса: https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    asyncio.run(web_crawler(URL))
