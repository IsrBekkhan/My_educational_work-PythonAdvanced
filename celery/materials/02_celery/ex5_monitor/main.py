from tasks import heavy_task


def get_factorial(arg):
    result = heavy_task.apply_async(args=(arg,))

    while not result.ready():
        # Задача еще выполняется
        pass

    if result.successful():
        result_value = result.get()
    else:
        # Информация об ошибке
        result_value = result.result

    print(result_value)


for i in range(100):
    get_factorial(10 * i)
