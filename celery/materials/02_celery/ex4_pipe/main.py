from celery import chain
from tasks import fetch_user_name, greeting_user

task1 = fetch_user_name.s(1)
task2 = greeting_user.s()

task_chain = chain(task1 | task2)
result = task_chain.apply_async()

final_result = result.get()
print(final_result)  # Здравствуй, Пётр 1-ый!
