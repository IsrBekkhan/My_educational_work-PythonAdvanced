from threading import Thread
from queue import PriorityQueue
from dataclasses import dataclass, field
from random import randint, random
from time import sleep

from typing import Callable, Any



@dataclass(order=True)
class Task:
    sort_index: int = field(init=False)

    priority: int
    fun: Callable
    args: tuple[Any]

    def __post_init__(self) -> None:
        self.sort_index = self.priority


SENTINEL_TASK: Task = Task(-1, lambda: None, (None,))


class Producer(Thread):
    TASKS_COUNT: int = 10

    def __init__(self, queue: PriorityQueue[Task]):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        print('Producer: Running')
        for i in range(self.TASKS_COUNT):
            task: Task = Task(
                priority=randint(0, 10),
                fun=sleep,
                args=(random(),)
            )
            queue.put(task)
        queue.join()
        queue.put(SENTINEL_TASK)
        print('Producer: Done')


class Consumer(Thread):
    def __init__(self, queue: PriorityQueue[Task]) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        print('Consumer: Running')
        while True:
            task: Task = self.queue.get()
            if task is SENTINEL_TASK:
                break

            priority: int = task.priority
            fun_name: str = task.fun.__name__
            args_str: str = ', '.join(map(str, task.args))
            print(f'>running Task(priority={priority}).\t\t{fun_name}({args_str})')

            task.fun(*task.args)
            self.queue.task_done()
        print('Consumer: Done')


queue: PriorityQueue[Task] = PriorityQueue()
producer = Producer(queue)
consumer = Consumer(queue)
producer.start()
consumer.start()

producer.join()
consumer.join()