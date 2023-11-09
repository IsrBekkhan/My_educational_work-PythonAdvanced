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
        task_index = 0

        for task_object in self.queue:

            if task_object.priority < task.priority:
                task_index = self.queue.index(task_object)
                self.queue.insert(task_index, task)
                break
        else:
            self.queue.append(task)

        if not self.queue:
            self.queue.insert(task_index, task)


    def execute_tasks(self) -> None:
        while self.queue:
            task = self.queue.popleft()
            print('Исполняется задача:', task, task.priority)
            task.execute()
        print('Все задачи были успешно выполнены')
        self.queue.clear()


if __name__ == '__main__':
    queue = TaskQueue()

    queue.add_task(Task(
        func=time.sleep,
        args=(1,),
        priority=1
    ))
    queue.add_task(Task(
        func=print,
        args=('Hello', 'World'),
        kwargs={'sep': '_'},
        priority=3
    ))
    queue.add_task(Task(
        func=math.factorial,
        args=(50,),
        priority=2
    ))

    queue.execute_tasks()

