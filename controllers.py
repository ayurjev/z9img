""" Контроллеры сервиса """

import json
import base64
from io import BytesIO
from envi import Controller as EnviController, Request
from exceptions import BaseAuthException
from models import ImageProcessor


def error_format(func):
    """ Декоратор для обработки любых исключений возникающих при работе сервиса
    :param func:
    """
    def wrapper(*args, **kwargs):
        """ wrapper
        :param args:
        :param kwargs:
        """
        try:
            return func(*args, **kwargs)
        except BaseAuthException as e:
            return json.dumps({"error": {"code": e.code}})
    return wrapper


class Controller(EnviController):
    """ Контроллер """

    @classmethod
    @error_format
    def resize(cls, request: Request, **kwargs):
        """ Метод для изменения размера изображения (масштабирование)
        :param request:
        :param kwargs:
        :return:
        """
        bytes_object = BytesIO(base64.b64decode(request.get("img").replace(" ", "+").encode()))
        converted = ImageProcessor(bytes_object).resize(request.get("width"), request.get("height"))
        return base64.b64encode(converted)

    @classmethod
    @error_format
    def crop(cls, request: Request, **kwargs):
        """ Метод для обрезки изображения
        :param request:
        :param kwargs:
        :return:
        """
        bytes_object = BytesIO(base64.b64decode(request.get("img").replace(" ", "+").encode()))
        converted = ImageProcessor(bytes_object).crop(json.loads(request.get("coords")), json.loads(request.get("from_size")))
        return base64.b64encode(converted.getvalue())