#### Шпаргалка по rsync

Синхронизация каталогов dir1 и dir2 на одной машине:

```shell
rsync -a dir1 dir2
```

Синхронизация удалённой системы:

```shell
rsync -a local_dir username@remote_host:remote_dir
``` 

В обратную сторону:

```shell
rsync -a username@remote_host:remote_dir local_dir
```

Использование с ключом:

```shell
rsync -e 'ssh -i timeweb' -Paz username@remote_host:remote_dir local_dir
```

Опции:<br>
−r — рекурсивная синхронизация.<br>
−a — режим архива, эквивалент -rlptgoD.<br>
−z — сжатие данных.<br>
−P — показать прогресс синхронизации.<br>
−e — используется для задания параметров при подключении через SSH.

Полный список опций можно найти в [документации](https://linux.die.net/man/1/rsync).