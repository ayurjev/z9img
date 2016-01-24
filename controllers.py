""" Контроллеры сервиса """

import json
import base64
from io import BytesIO
from envi import Controller as EnviController, Request
from exceptions import BaseServiceException
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
        except BaseServiceException as e:
            return json.dumps({"error": {"code": e.code, "message": str(e)}})
        except Exception as e:
            return json.dumps({"error": {"code": None, "message": str(e)}})
    return wrapper


class Controller(EnviController):
    """ Контроллер """

    @classmethod
    @error_format
    def scale(cls, request: Request, **kwargs):
        """ Метод для изменения размера изображения (масштабирование)
        :param request:
        :param kwargs:
        :return:
        """
        bytes_object = BytesIO(base64.b64decode(request.get("base64").replace(" ", "+").encode()))
        converted = ImageProcessor(bytes_object).scale(request.get("size"))
        return {"base64": base64.b64encode(converted.getvalue()).decode()}

    @classmethod
    @error_format
    def crop(cls, request: Request, **kwargs):
        """ Метод для обрезки изображения
        :param request:
        :param kwargs:
        :return:
        """
        bytes_object = BytesIO(base64.b64decode(request.get("base64").replace(" ", "+").encode()))
        converted = ImageProcessor(bytes_object).crop(request.get("coords"), request.get("from_size"))
        return {"base64": base64.b64encode(converted.getvalue()).decode()}