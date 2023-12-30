import asyncio
import inspect

from typing import Iterable, Iterator, Generator, Awaitable, Coroutine


@asyncio.coroutine
def old_coroutine():
    print("It's old coroutine")
    yield from asyncio.sleep(2)


async def new_coroutine():
    print("It's new coroutine")
    await asyncio.sleep(2)


print('Iterator:', isinstance(old_coroutine(), Iterator))
print('Iterable', isinstance(old_coroutine(), Iterable))
print('Generator', isinstance(old_coroutine(), Generator))
print('Awaitable', isinstance(old_coroutine(), Awaitable))
print('Coroutine', isinstance(old_coroutine(), Coroutine))

print()

print('Iterator:', isinstance(new_coroutine(), Iterator))
print('Iterable', isinstance(new_coroutine(), Iterable))
print('Generator', isinstance(new_coroutine(), Generator))
print('Awaitable', isinstance(new_coroutine(), Awaitable))
print('Coroutine', isinstance(new_coroutine(), Coroutine))

print('-' * 100)

print('Is coroutine:', asyncio.iscoroutine(old_coroutine()))
print('Is coroutine:', asyncio.iscoroutine(new_coroutine()))

print()

print('Is coroutine (inspect):', inspect.iscoroutine(old_coroutine()))
print('Is coroutine (inspect):', inspect.iscoroutine(new_coroutine()))

print('-' * 100)

print('Is awaitable:', inspect.isawaitable(old_coroutine()))
print('Is awaitable:', inspect.isawaitable(new_coroutine()))

