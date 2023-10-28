from celery import group
from tasks import buy_milk, buy_bread

task1 = buy_milk.s(1)
task2 = buy_bread.s(5)

task_group = group(task1, task2)
result = task_group.apply_async()

results = result.get()
print(results)  # [1, 3]
