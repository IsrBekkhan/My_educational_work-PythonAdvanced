import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Tuple, Dict


@dataclass
class Task:
    func: Callable
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    priority: int = field(default=1)

    def execute(self) -> None:
        self.func(*self.args, **self.kwargs)

    def __str__(self):
        task_str = self.func.__name__ + '('

        f_args = ', '.join(map(repr, self.args))
        task_str += f_args

        if self.kwargs:
            f_kwargs = ', '.join(
                f'{k}={v!r}' for k, v in self.kwargs.items()
            )
            task_str += ', ' + f_kwargs

        task_str += ')'
        return task_str


class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task: Task) -> None:
        print('Добавлена задача:', task)
        self.queue.append(task)

    def execute_tasks(self) -> None:
        while self.queue:
            task = self.queue.popleft()
            print('Исполняется задача:', task)
            task.execute()
        print('Все задачи были успешно выполнены')


if __name__ == '__main__':
    queue = TaskQueue()
    queue_list = list()

    queue_list.append(Task(
        func=time.sleep,
        args=(1,),
        priority=1
    ))
    queue_list.append(Task(
        func=print,
        args=('Hello', 'World'),
        kwargs={'sep': '_'},
        priority=10
    ))
    queue_list.append(Task(
        func=math.factorial,
        args=(50,),
        priority=3
    ))
    sorted_list = sorted(queue_list, key=lambda task: task.priority, reverse=True)

    for task in sorted_list:
        queue.add_task(task)

    queue.execute_tasks()

