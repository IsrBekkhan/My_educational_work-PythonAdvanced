"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

docs/simple.txt:
hello world!

/preview/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/preview/100/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""

from flask import Flask
from os.path import abspath, exists, join

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str):
    project_path = abspath('')
    relative_path_list = relative_path.split('/')
    file_abs_path = join(project_path, *relative_path_list)

    if exists(file_abs_path):

        with open(file_abs_path, 'r') as text_file:
            result_text = text_file.read(size)
            result_size = len(result_text)
            status_code = 200

            return f'<b>{file_abs_path}</b> {result_size}<br>{result_text}', status_code

    status_code = 404
    return 'Файл не найден', status_code


if __name__ == "__main__":
    app.run(debug=True)
