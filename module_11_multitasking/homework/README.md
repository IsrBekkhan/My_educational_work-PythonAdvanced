# Практическая работа, модуль 11

## Цели практической работы

* Научиться:
    * создавать многопоточные программы на Python;
    * делать параллельные запросы к API с помощью requests;
    * использовать примитивы синхронизации.
* Познакомиться с приоритетной очередью.

## Что входит в практическую работу

1. Философы.
2. Звёздные войны.
3. Печатный станок.
4. Приоритетная очередь.

## Задача 1. Философы

### Что нужно сделать

Вернёмся к задаче об обедающих философах.

Пять философов сидят вокруг круглого стола, перед каждым философом стоит тарелка спагетти. Вилки лежат на столе между
каждой парой ближайших философов.

Каждый философ может либо есть, либо размышлять. Однако философ может есть только тогда, когда держит две вилки — взятую
справа и слева.

В последнем занятии мы решили эту проблему. Перепишите задачу так, чтобы вместо явного вызова методов захвата и
освобождения использовался контекстный менеджер.

```python
import logging
import threading
import random
import time
from typing import List

logging.basicConfig(level='INFO')
logger: logging.Logger = logging.getLogger(__name__)


class Philosopher(threading.Thread):
    running: bool = True

    def __init__(self, left_fork: threading.Lock, right_fork: threading.Lock) -> None:
        super().__init__()
        self.left_fork: threading.Lock = left_fork
        self.right_fork: threading.Lock = right_fork

    def run(self) -> None:
        while self.running:
            logger.info(f'Philosopher {self.name} start thinking.')
            time.sleep(random.randint(1, 10))
            logger.info(f'Philosopher {self.name} is hungry.')
            try:
                self.left_fork.acquire()
                logger.info(f'Philosopher {self.name} acquired left fork')
                if self.right_fork.locked():
                    continue
                try:
                    self.right_fork.acquire()
                    logger.info(f'Philosopher {self.name} acquired right fork')
                    self.dining()
                finally:
                    self.right_fork.release()
            finally:
                self.left_fork.release()

    def dining(self) -> None:
        logger.info(f'Philosopher {self.name} starts eating.')
        time.sleep(random.randint(1, 10))
        logger.info(f'Philosopher {self.name} finishes eating and leaves to think.')


def main() -> None:
    forks: List[threading.Lock] = [threading.Lock() for n in range(5)]
    philosophers: List[Philosopher] = [
        Philosopher(forks[i % 5], forks[(i + 1) % 5])
        for i in range(5)
    ]
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(200)
    Philosopher.running = False
    logger.info("Now we're finishing.")


if __name__ == "__main__":
    main()
```

### Что оценивается

* Используется только контекстный менеджер.

## Задача 2. Звёздные войны

### Что нужно сделать

1. Потренируйтесь с новым модулем requests. Скачайте 20
   персонажей [из базы данных о «Звёздных войнах»](https://swapi.dev/) и сохраните их имена, возраст, пол в БД. Замерьте
   время работы программы.
2. Добавьте потоки. Замерьте время работы и сравните результаты.
3. Оформите решение в виде двух функций, чтобы можно было протестировать производительность обоих вариантов.

### Советы и рекомендации

* Чтобы получить результат запроса, обратитесь к методу `json()` объекта `Response`.

### Что оценивается

* Для решения используются потоки, а не процессы.
* Решение оформлено в виде двух отдельных функций — с использованием последовательных и параллельных запросов.
* Время работы замеряется в коде.
* Информация о персонажах записывается в БД.

## Задача 3. Печатный станок

### Что нужно сделать

Вернёмся к задаче с продавцами билетов.

В кинотеатре открыты три кассы. Пока хотя бы одна из них свободна, человек может купить себе билет. Но если все три
кассы заняты, то ему нужно подождать в очереди.

Добавьте в задачу ещё одного персонажа — главного директора с печатным станком. По условию, как только количество
проданных билетов приближается к такому, что каждый из продавцов сможет продать не более одного, то в этот момент
директор должен добавить в общее число доступных билетов ещё сколько-то.

Пример: осталось четыре билета, директор добавляет шесть, всего билетов десять. Пусть директор может так делать, пока
общее количество билетов не превысит общее число посадочных мест.

Пока директор пополняет билеты, продавцы не могут их продавать.

```python
import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
```

### Советы и рекомендации

* Обратите внимание на пороговое значение, при котором директор начнёт печатать билеты, чтобы избежать ситуации
  досрочного завершения работы продавцов.

### Что оценивается

* Для директора создан свой класс, наследуемый от класса `Thread`.
* Для продавцов и директора используется один семафор.

## Задача 4. Приоритетная очередь

### Что нужно сделать

Приоритетная очередь — очередь, где у каждого элемента есть приоритет. Элемент с более высоким приоритетом находится
перед элементом с более низким приоритетом. Эту структуру данных реализует
класс [PriorityQueue](https://docs.python.org/3/library/queue.html#queue.PriorityQueue) из
модуля [queue](https://docs.python.org/3/library/queue.html#module-queue).

Создайте два класса, наследуемые от класса `Thread`: `Producer` и `Consumer`. Первый будет генерировать задачи и класть
их в очередь, второй — брать задачу с наивысшим приоритетом и исполнять её.

Для упрощения работы сделайте так, чтобы `Producer` сначала добавил все задачи в очередь, а только затем `Consumer`
исполнил их.

Результат работы программы должен получиться примерно таким:

```
Producer: Running
Consumer: Running
>running Task(priority=0).          sleep(0.019658567230089852)
>running Task(priority=0).          sleep(0.8260261640443046)
>running Task(priority=1).          sleep(0.5049788914608555)
>running Task(priority=1).          sleep(0.9939451305978486)
>running Task(priority=2).          sleep(0.6217303299399963)
>running Task(priority=2).          sleep(0.7283236739267553)
>running Task(priority=3).          sleep(0.13090364153051426)
>running Task(priority=3).          sleep(0.21140406953974167)
>running Task(priority=4).          sleep(0.8426715099235477)
>running Task(priority=6).          sleep(0.43248434769420785)
Producer: Done
Consumer: Done
```

### Советы и рекомендации

* Для решения задачи вам понадобятся четыре метода объекта PriorityQueue:
    * [put](https://docs.python.org/3/library/queue.html#queue.Queue.put) — добавляет элемент (priority, value) в
      очередь;
    * [get](https://docs.python.org/3/library/queue.html#queue.Queue.get) — берёт элемент с наивысшим приоритетом и
      удаляет его из очереди;
    * [task_done](https://docs.python.org/3/library/queue.html#queue.Queue.task_done) — указывает, что задача была
      выполнена;
    * [join](https://docs.python.org/3/library/queue.html#queue.Queue.join) — блокирует очередь, пока все задачи не
      будут выполнены.
* Чтобы проверить, выполнены ли все задачи, можно использовать метод `queue.empty()` либо добавить мнимую задачу None в
  качестве сигнального значения для `Consumer`.

### Что оценивается

* `Producer` и `Consumer` являются потомками класса Thread.
* `Producer` и `Consumer` не знают друг о друге. В конструкторе они принимают объект `PriorityQueue`.
* Модель задачи выделена в отдельный класс или функцию.

## Общие советы и рекомендации

* Для синхронизации доступа к ресурсам мы рассмотрели лишь два объекта: `Lock` и `Semaphore`, — но есть ещё и другие из
  модуля `threading`. О них вы можете прочитать в
  статье [«Потоки и процессы в Python. Часть 2. Синхронизация потоков»](https://devpractice.ru/python-lesson-23-concurrency-part-2/)
  .

## Что оценивается в практической работе

* Названия переменных, функций и классов имеют значащие имена.
* Для обеспечения параллельной работы потоков `join()` делается после того, как все потоки оказываются запущены.
* Использование общих ресурсов происходит в блоке синхронизации доступа.
