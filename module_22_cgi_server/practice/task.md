### 1

Прочитать:
* https://ekaterinagoltsova.github.io/posts/apache-vs-nginx/
* https://russianblogs.com/article/2327952228/


### 2

Мы сделали autoindex на всю директорию с сайтом. Это не слишком безопасно и красиво. Почти `from foo import *`. Давайте это исправим. Добавьте еще одну директиву location, где мы добавим autoindex только на папку с картинками