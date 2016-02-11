""" Модели """

from io import BytesIO
from PIL import Image


class ImageProcessor(object):
    """ Класс для работы с изображениями """

    def __init__(self, image_bytes: BytesIO):
        self.image_bytes = image_bytes

    def scale(self, size: int) -> BytesIO:
        """ Метод для изменение размера изображения
        :param size: Размер большей стороны изображения
        :return:
        """
        size = int(size)
        img = Image.open(self.image_bytes)
        k = img.width / img.height
        if img.width > img.height:
            width = size
            height = k * width
        else:
            height = size
            width = k * height

        img.thumbnail((int(width), int(height)), Image.ANTIALIAS)
        b = BytesIO()
        img = img.convert('RGB')
        img.save(b, "JPEG", quality=85)
        print(len(b.getvalue()))
        return BytesIO(b.getvalue())

    def crop(self, box: dict, from_size: dict=None) -> BytesIO:
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
        b = BytesIO()
        img = img.convert('RGB')
        img.save(b, "JPEG", quality=100)
        return BytesIO(b.getvalue())

