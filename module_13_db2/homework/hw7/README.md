## Задача 7. Делаем инъекцию

### Что нужно сделать

Мы часто говорили о важности параметризованных запросов и упоминали понятие SQL-инъекции. Давайте взглянем на это со
стороны хакера.

В таблице `table_users` имена и пароли пользователей. Также есть функция `register`, она регистрирует пользователя,
добавляя запись в эту таблицу. Функцию писал неопытный и наивный программист, поэтому в ней есть уязвимые места.

```python
import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()
```

Ваша задача — задать переменным `username` и `password` в функции `hack` такие значения, чтобы с таблицей произошло
нечто страшное. Например, её удаление или добавление очень большого количества новых записей.

```python
def hack() -> None:
    username: str = "i_like"
    password: str = "sql_injection"
    register(username, password)
```

### Советы и рекомендации

* [Методы execute, executemany и executescript](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor)
* Подумайте, какие две основные ошибки допустил неопытный программист в функции `register`.

### Что оценивается

* Для взлома используются только строковые значения переменных username и password.
* Таблица претерпела серьёзные изменения, которые дали неопытному программисту ценный урок в виде:
    * удаления таблицы или записей;
    * изменения существующих записей;
    * добавления большого числа новых записей;
    * [изменения схемы таблицы](https://www.sqlitetutorial.net/sqlite-alter-table/).
