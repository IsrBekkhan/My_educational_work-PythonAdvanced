from typing import List, Optional, Union
from datetime import datetime
from typing import List, Optional

from flask import Flask, request

app = Flask(__name__)


# http://127.0.0.1:5000/search/?cell_tower_id=50&phone_prefix=999*&
# protocol=4G&signal_level=-50.5&date_from=20120513&date_to=20230510
@app.route(
    "/search/", methods=["GET"],
)
def search():
    cell_tower_ids: List[int] = request.args.getlist("cell_tower_id", type=int)

    for cell_tower_id in cell_tower_ids:

        if cell_tower_id <= 0:
            return 'Cell_tower_id не может быть меньше 0', 400

    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    phone_prefixes: List[str] = request.args.getlist("phone_prefix")

    for phone_prefix in phone_prefixes:

        if phone_prefix[-1] != '*' or not phone_prefix[0:-1].isdigit():
            return 'phone_prefix должен состоять из чисел и заканчиваться звёздочкой', 400

        if len(phone_prefix) > 11:
            return 'Чисел в phone_prefix должно быть не больше, чем 10', 400

    protocols: List[str] = request.args.getlist("protocol")

    for protocol in protocols:

        if not protocol in ('2G', '3G', '4G'):
            return 'Несуществующий протокол', 400

    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None
    )

    date_from: Optional[int] = request.args.get(
        'date_from', type=int, default=None
    )

    date_to: Optional[int] = request.args.get(
        'date_to', type=int, default=None
    )

    date_from_obj = datetime.strptime(str(date_from), '%Y%m%d')
    date_to_obj = datetime.strptime(str(date_to), '%Y%m%d')

    if not all((date_from_obj < datetime.today(), date_to_obj < datetime.today(), date_from_obj < date_to_obj)):
        return 'Введите реальные значения дат', 400

    return (
        f"Search for {cell_tower_ids} cell towers. Search criteria: "
        f"phone_prefixes={phone_prefixes}, "
        f"protocols={protocols}, "
        f"signal_level={signal_level}, "
        f'date_from={str(date_from)}, '
        f'date_to={str(date_to)} '
        f"signal_level={signal_level}"
    )


@app.route('/array/', methods=['GET'])
def array() -> str:
    array_list: List[int] = request.args.getlist('num', type=int)
    mult_result = 1

    for num in array_list:
        mult_result *= num

    array_sum = sum(array_list)

    return (
        f'Сумма чисел {array_list} = {array_sum}, '
        f'произведение = {mult_result}'
    )


@app.route('/combinations/', methods=['GET'])
def combination() -> str:
    nums_a: List[int] = request.args.getlist('num_a', type=int)
    nums_b: List[int] = request.args.getlist('num_b', type=int)
    combinations = list()

    for a in nums_a:
        for b in nums_b:
            combinations.append(int(f'{a}{b}'))

    return f'Все возможные комбинации пар чисел a = {nums_a} и b = {nums_b}: <b>{combinations}</b>'


@app.route('/to_close/', methods=['GET'])
def to_close() -> str:
    nums: List[int] = request.args.getlist('nums', type=int)
    num_x: int = request.args.get('num_x', type=int)

    nums_temp = nums.copy()
    nums_temp.append(num_x)
    nums_sorted = sorted(nums_temp)
    num_x_id = nums_sorted.index(num_x)

    if num_x_id == 0:
        to_close_num = nums_sorted[num_x_id + 1]
    elif len(nums_sorted) - 1 == num_x_id:
        to_close_num = nums_sorted[num_x_id - 1]
    elif (num_x - nums_sorted[num_x_id - 1]) < (nums_sorted[num_x_id + 1] - num_x):
        to_close_num = nums_sorted[num_x_id - 1]
    else:
        to_close_num = nums_sorted[num_x_id + 1]

    return f'Максимально близкое к числу {num_x} число из массива {nums}: <b>{to_close_num}</b>'


if __name__ == "__main__":
    app.run(debug=True)

