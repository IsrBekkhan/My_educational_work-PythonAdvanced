from dataclasses import dataclass, field
from typing import Any

from queue import PriorityQueue
from threading import Thread

from time import sleep
from random import random, randint


class Producer(Thread):

    def __init__(self, queue: PriorityQueue):
        super(Producer, self).__init__()
        self.queue = queue

    def run(self):
        print('Producer: Running')

        for _ in range(10):
            rand_priority = randint(0, 10)
            self.queue.put(Task(priority=rand_priority))

        print('Producer: Done')


class Consumer(Thread):

    def __init__(self, queue: PriorityQueue):
        super(Consumer, self).__init__()
        self.queue = queue

    def run(self):
        print('Consumer: Running')

        for _ in range(10):
            task = self.queue.get()
            task.run_task()

        print('Consumer: Done')


@dataclass(order=True)
class Task:
    priority: int
    item: Any = field(compare=False)

    def __init__(self, priority):
        self.priority = priority

    def run_task(self):
        sleep_time = random()
        print(f'>running Task(priority={self.priority}). \t\t sleep({sleep_time})')
        sleep(sleep_time)


if __name__ == '__main__':
    p_queue = PriorityQueue()
    Producer(queue=p_queue).start()
    Consumer(queue=p_queue).start()

