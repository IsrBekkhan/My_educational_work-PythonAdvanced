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
