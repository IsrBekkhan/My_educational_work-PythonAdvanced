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
