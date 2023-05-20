"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> str:
    numbers_list = numbers.split('/')

    for elem in numbers_list:

        if not elem.isdigit():
            return 'Ошибка обработки запроса: введено нечисловое значение'

    numbers_list = map(int, numbers_list)

    return f'Максимальное число: {max(numbers_list)}'


if __name__ == "__main__":
    app.run(debug=True)
