### Практика. Урок 1: 
Прочитать: 
* https://habr.com/ru/post/337528/
* https://developer.mozilla.org/ru/docs/Learn/JavaScript/Asynchronous/Concepts


### Практика. Урок 2:
* Лучше один раз увидеть, чем сто раз услышать: прочитайте в документации о генераторах
https://docs.python.org/3/reference/expressions.html#yield-expressions (англ)
* Потренируйтесь в новом синтаксисе: повторите примеры с yield from. Попробуйте добавить туда итерацию из коллекций и других генераторов

### Практика. Урок 3:

О некоторых отличиях старых и новых корутин мы все же умолчали. Проверьте оба типа корутин функцией isinstance на следующие классы из модуля typing:
* Iteratorable
* Generator
* Awaitable
* Coroutine

Так же воспользуйтесь этими функциями:
* asyncio.iscoroutine()
* inspect.iscoroutine()
* inspect.isawaitable()

Найдите все отличия. Они - прямое следствие эволюционного развития python и того, как в нем менялось понимание того, что такое корутина.
