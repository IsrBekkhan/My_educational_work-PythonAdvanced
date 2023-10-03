from flasgger import swag_from
from typing import Callable
import json


def swag_from_json(json_file: str) -> Callable:

    def convert_to_dict(func: Callable) -> Callable:
        with open(json_file, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)

        @swag_from(data)
        def wrapped_func(*args, **kwargs) -> Callable:
            return func(*args, **kwargs)

        return wrapped_func

    return convert_to_dict
