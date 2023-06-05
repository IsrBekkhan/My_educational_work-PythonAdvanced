
***

### Ошибка №1: NameError: name 'address' is not defined

***

### *Текст исключения:*
Error
Traceback (most recent call last):
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\tests\test_person.py", line 39, in test_can_check_is_homeless
    self.assertEqual(is_homeless, self.person.is_homeless())
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\person.py", line 28, in is_homeless
    return address is None
           ^^^^^^^
NameError: name 'address' is not defined

### *Код с ошибкой:*

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return address is None

### *Исправленный код:*

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return self.address is None

***

### Ошибка №2: NameError: name 'datetime' is not defined

***

### *Текст исключения:*

Error
Traceback (most recent call last):
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\tests\test_person.py", line 16, in test_can_get_age
    self.assertEqual(age, self.person.get_age())
                          ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\person.py", line 9, in get_age
    now: datetime.datetime = datetime.datetime.now()
                             ^^^^^^^^
NameError: name 'datetime' is not defined

### *Решение:*

	import datetime

***

### Ошибка №3: AssertionError: 'Грозный' != 'Город'

***

### *Текст исключения:*

Город != Грозный

Expected :Грозный
Actual   :Город
<Click to see difference>

Traceback (most recent call last):
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\tests\test_person.py", line 30, in test_can_set_address
    self.assertEqual(address, self.person.address)
AssertionError: 'Грозный' != 'Город'
- Грозный
+ Город


### *Код с ошибкой:*

    def set_address(self, address: str) -> None:
        self.address == address

### *Исправленный код:*

    def set_address(self, address: str) -> None:
        self.address = address

***

### Ошибка №4: AssertionError: 'Бекхан' != 'Имя'

***

### *Текст исключения:*

Имя != Бекхан

Expected :Бекхан
Actual   :Имя
<Click to see difference>

Traceback (most recent call last):
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\tests\test_person.py", line 25, in test_can_set_name
    self.assertEqual(name, self.person.name)
AssertionError: 'Бекхан' != 'Имя'
- Бекхан
+ Имя

### *Код с ошибкой:*

    def set_name(self, name: str) -> None:
        self.name = self.name

### *Исправленный код:*

    def set_name(self, name: str) -> None:
        self.name = name

***

### Ошибка №5: AssertionError: 33 != -33

***

### *Текст исключения:*

-33 != 33

Expected :33
Actual   :-33
<Click to see difference>

Traceback (most recent call last):
  File "C:\Users\Bekkhan\PycharmProjects\python_advanced\module_03_ci_culture_beginning\homework\hw4\tests\test_person.py", line 16, in test_can_get_age
    self.assertEqual(age, self.person.get_age())
AssertionError: 33 != -33

### *Код с ошибкой:*

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return self.yob - now.year

### *Исправленный код:*

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return now.year - self.yob



