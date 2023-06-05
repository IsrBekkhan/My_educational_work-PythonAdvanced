## Задача 2. Удалённое исполнение кода
### Что нужно сделать
Напишите endpoint, который принимает на вход код на Python (строка) и тайм-аут в секундах (положительное число не больше 30). Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло, то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.

Тесты к заданию обязательны.
### Советы и рекомендации
- Чтобы запустить код, используйте такой синтаксис:

`python -c "code"`

Например, `python -c "print('Hello world!')"`
- Для выполнения задания рекомендуется использовать метод [Popen.communicate](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate).
- Чем может грозить использование параметра s`hell=True`:
```jupyterpython
>>>  code = 'print()"; echo "hacked'
>>> cmd = f'python -c "{code}"'
>>> Popen(cmd, shell=True)
<Popen: returncode: None args: 'python -c "print()"; echo "hacked"'>
>>>
hacked
```
- Однако есть ещё одна проблема — мы можем запустить сторонний процесс в самом коде:  
```shell
$ python -c "
from subprocess import run
run(['./kill_the_system.sh'])
"
Hello from kill_the_system.sh
```
Чтобы защититься от этого, нужно наложить ограничения на ресурсы, которые может использовать запускаемая программа. Сделать это можно с помощью встроенной утилиты `prlimit`:

```shell
$ prlimit --nproc=1:1 python -c "
from subprocess import run
run(['./kill_the_system.sh'])
"
BlockingIOError: [Errno 11] Resource temporarily unavailable
```
### Что оценивается
- Endpoint принимает POST-запрос.
- Используется FlaskForm с валидаторами для полей.
- Написаны тесты для следующих случаев:
  - Тайм-аут ниже, чем время исполнения.
  - Некорректно введённые данные в форме.
  - Небезопасный ввод в поле с кодом (проверка на `shell=True`).
