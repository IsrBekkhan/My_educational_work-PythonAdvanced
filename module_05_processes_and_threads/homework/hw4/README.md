## Задача 4. Перенаправление вывода
### Что нужно сделать
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения. Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы) и перенаправляет туда стандартные потоки stdout и stderr. 

Аргументы контекстного менеджера должны быть непозиционными, чтобы можно было ещё перенаправить только stdout или только stderr.

Тесты к заданию обязательны.

#### Пример
**Код**
```python
print('Hello stdout')
stdout_file = open('stdout.txt', 'w')
stderr_file = open('stderr.txt', 'w')

with Redirect(stdout=stdout_file, stderr=stderr_file):
    print('Hello stdout.txt')
    raise Exception('Hello stderr.txt')

print('Hello stdout again')
raise Exception('Hello stderr')
```

**Стандартный поток**
```
Hello stdout
Hello stdout again
Traceback (most recent call last):
  File "/home/wignorbo/tmp", line 30, in <module>
    raise Exception('Hello stderr')
Exception: Hello stderr
```

**stdout.txt**
```
Hello stdout.txt
```

**stderr.txt**
```
Traceback (most recent call last):
  File "/home/wignorbo/tmp", line 27, in <module>
    raise Exception('Hello stderr.txt')
Exception: Hello stderr.txt
```
### Советы и рекомендации
- [Интерфейс класса IOBase](https://docs.python.org/3/library/io.html#io.IOBase).
- В ходе тестирования могут возникнуть конфликты из-за перехвата стандартного потока вывода. Чтобы этого избежать, результаты юнит-тестов можно перенаправить, например, так:
    ```python
    if __name__ == '__main__':
        with open('test_results.txt', 'a') as test_file_stream:
            runner = unittest.TextTestRunner(stream=test_file_stream)
            unittest.main(testRunner=runner)
    ```
- Чтобы вывести полный текст ошибки, понадобится модуль traceback:
    ```python
    import traceback
    sys.stderr.write(traceback.format_exc())
    ```
### Что оценивается
- В тестах проверяется, что информация действительно была перенаправлена в другой поток вывода.
- При инициализации контекстного менеджера сохраняются предыдущие значения `sys.stdout` и `sys.stderr`. При использовании `sys.__stdout__` и `sys.__stderr__` могут не работать вложенные блоки.
- Учтены случаи использования контекстного менеджера без аргументов или только с одним аргументом — `stdout` или `stderr`.
