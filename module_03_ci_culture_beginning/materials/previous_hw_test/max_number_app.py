from typing import List

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> tuple[str, int]:
    numbers_split: List[str] = numbers.split('/')
    try:
        max_number: float = max(map(int, numbers_split))
        return f'Максимальное число: <i>{max_number}</i>', 200
    except ValueError:
        return "Переданы некорректные значения", 400


if __name__ == "__main__":
    app.run(debug=True)
