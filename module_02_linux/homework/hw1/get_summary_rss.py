"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    total_size = 0
    description = 'Объём потребляемой памяти'

    with open(ps_output_file_path, 'r') as output_file:
        lines = output_file.readlines()[1:]
        bytes_in_kb = 1024
        bytes_in_mb = 1048576
        bytes_in_gb = 1073741824

        for line in lines:

            if len(line) > 4:
                line_elements = line.split()
                total_size += int(line_elements[5])

        if total_size <= bytes_in_kb:
            return f'{description}: {total_size} B'

        if total_size <= bytes_in_mb:
            size = total_size / bytes_in_kb
            return f'{description}: {int(size)} kB'

        if total_size <= bytes_in_gb:
            size = total_size / bytes_in_mb
            return f'{description}: {int(size)} MB'

        if total_size > bytes_in_gb:
            size = total_size / bytes_in_gb
            return f'{description}: {int(size)} GB'


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
