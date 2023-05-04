## Задача 5. Система сборки (выполните по желанию)
### Что нужно сделать
Напишите bash-скрипт для задания №2, который при запуске выполнит следующие действия:

1. Проверит код программы с помощью статического анализатора [pylint](https://pylint.pycqa.org/en/latest/tutorial.html).<br>Результат должен сохраняться в JSON-файл, а в консоль должны выводиться отчёт и метрика качества кода.
2. Запустит юнит-тесты для программы.
3. Если предыдущие шаги выполнены успешно, выведет сообщение ОК, иначе — «Имеются ошибки».

Сделайте несколько ошибок в коде, чтобы посмотреть, как меняется вывод.

### Советы и рекомендации
- [Шпаргалка по написанию bash-скриптов](https://gist.github.com/Titiaiev/dcb7298389d1276b823bbc96e29f940d)
- Библиотека `pylint` позволяет проверить исходный код, найти ошибки и оценить качество написанной программы. Установка:

`pip3 install pylint`

Запуск:

`pylint program.py`

Вам пригодятся несколько флагов: [output-format](https://pylint.pycqa.org/en/latest/user_guide/usage/output.html?highlight=output-format#output-options), [reports](https://pylint.pycqa.org/en/latest/user_guide/usage/output.html#reports-section), [score](https://pylint.pycqa.org/en/latest/user_guide/usage/output.html#score-section).
- `subTest` принимает в качестве входных параметров сообщение и именованные аргументы.

```python
for i range(10):
    with self.subTest('Test message' , n=i):
        self.assertEqual(expected, output)
```
`FAIL: test_decrypt (test_decrypt.DecryptTestCase) [Test message] (n=2)`

- Если при запуске скрипта выводится ошибка Permission denied, нужно дать этому файлу разрешение на запуск:

```
$ ./script.sh
Permission denied: ./script.sh
$ chmod u+x ./script.sh
$ ./script.sh
```
- Пример определения кода возврата:

```shell
pylint file.py
pylint_res=$?
if [[ pylint_res -eq 0 ]]; then
  echo 'Pylint OK'
else
  echo 'Pylint not OK'
fi
```
[Про коды возврата в Pylint](https://pylint.pycqa.org/en/latest/user_guide/usage/run.html#exit-codes)
### Что оценивается
- Формат вывода статического анализатора соответствует условию.
- Написан работающий bash-скрипт, с помощью которого запускаются статический анализатор и тесты.
- Внутри скрипта делается проверка кодов возврата исполненных команд.
