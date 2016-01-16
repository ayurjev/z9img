""" Модели """

from io import BytesIO
from PIL import Image


class ImageProcessor(object):
    """ Класс для работы с изображениями """

    def __init__(self, image_bytes: BytesIO):
        self.image_bytes = image_bytes

    def resize(self, width: int, height: int) -> bytes:
        """ Метод для изменение размера изображения
        :param width:
        :param height:
        :return:
        """
        img = Image.open(self.image_bytes)
        img.thumbnail((width, height), Image.ANTIALIAS)
        b= BytesIO()
        img.save(b, "JPEG", quality=85)
        return BytesIO(b.getvalue())

    def crop(self, box: dict, from_size: dict=None) -> bytes:
        """ Метод для обрезки изображения
        :param box: Координаты обрезки в виде {x: 0, y: 0, x2: 0, y2: 0, w: 100, h: 100}
        :param from_size: Размеры изображения, относительно которого даны координаты в box в виде {w: 100, h: 50}
        Если не переданы, то параметры берутся из размеров переданного в обработку изображения
        :return:
        """
        box = (int(box["x"]), int(box["y"]), int(box["x2"]), int(box["y2"]))
        img = Image.open(self.image_bytes)
        if from_size:
            scale_factor = img.width/(int(from_size["w"]) if from_size.get("w") and int(from_size["w"]) else img.width)
            box = [int(i*scale_factor) for i in box]
        img = img.crop(box)
        b= BytesIO()
        img.save(b, "JPEG", quality=100)
        return BytesIO(b.getvalue())

