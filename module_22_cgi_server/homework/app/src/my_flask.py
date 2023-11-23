from typing import Callable
from re import fullmatch, sub
import http


class SimplestWSGIApp:
    """
    Простейшее WSGI-приложение.

    >> app = SimplestWSGIApp()
    >>
    >> @app.route(r"/hello")
    >> def hello():
    >>     return "<h1>Hello</h1>", 200
    """

    def __init__(self):
        # маршруты
        self.routes: list[tuple[str, Callable]] = list()

    @staticmethod
    def __url_to_pattern(url_: str) -> str:
        """
        Заменяет переменные (если есть) в строке url
        на элементы регулярного выражения

        :param url_: шаблон url.
        """
        if '<' in url_ and '>' in url_:
            return sub('<\w+>', r'\\w+', url_)
        return url_

    def route(self, url_: str) -> Callable:
        """
        Связывает маршрут с его представлением
        и добавляет его как кортеж в список эндпоинтов

        """
        def decorator(func: Callable) -> Callable:
            self.routes.append(
                (self.__url_to_pattern(url_), func)
            )
            return func

        return decorator

    def __dispatch(self, request_url: str):
        """
        Ищет url-запроса среди эндпоинтов и возвращает ответ
        найденного эндпоинта.

        :param request_url: url запроса
        :return: тело ответа (str), статус-код (int)
        """
        headers = [('Content-type', 'text/plain')]

        for url_pattern, func in self.routes:
            if fullmatch(url_pattern, request_url):
                variables = self.__contains_variables(url_pattern, request_url)

                if variables is not None:
                    body, status = func(*variables)
                else:
                    body, status = func()

                return body, status, headers

        return 'По данному URL ничего не найдено', 404, headers

    @staticmethod
    def __contains_variables(pattern_: str, http_url: str):
        """
        Возвращает список со значениями переменных из url запроса

        """
        pattern_elems, url_elems = pattern_.split('/'), http_url.split('/')

        variables = list()

        for index in range(len(pattern_elems)):
            if pattern_elems[index] != url_elems[index]:
                variables.append(url_elems[index])

        if variables:
            return variables
        return None

    def __call__(self, environ: dict, start_response: Callable):
        """
        WSGI-приложение

        """
        body, status_code, headers = self.__dispatch(environ["REQUEST_URI"])

        http_status_code = http.HTTPStatus(status_code)
        start_response(
            f"{http_status_code.value} {http_status_code.phrase}",
            headers
        )

        if body is None:
            return [b""]

        if not body.endswith("\n"):
            body += "\n"
        return [body.encode('utf-8')]


