## Задача 3. Прерывание программы

### Что нужно сделать

Внесите изменения в следующую программу так, чтобы её можно было прервать с помощью `Ctrl+C`, корректно завершив потоки `t1` и `t2`:

```python
from threading import Semaphore, Thread
import time

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)
try:
    t1.start()
    t2.start()
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    exit(1)
```

### Советы и рекомендации

Вероятно, в интернете вы найдёте много вариантов решения этой задачи. Выберите несколько и подумайте, какой из них лучше
и почему.

### Что оценивается

* Функции `fun1()` и `fun2()` не претерпели изменений.
* При нажатии `Ctrl+C` программа завершает работу потоков.
