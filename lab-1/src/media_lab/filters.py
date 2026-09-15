"""Абстрактные и конкретные фильтры изображений."""

from abc import ABC, abstractmethod

from PIL import Image as PILImage
from PIL import ImageEnhance
from PIL import ImageFilter as PILImageFilter


class ImageFilter(ABC):
    """Абстрактный интерфейс фильтра изображения."""

    @abstractmethod
    def apply(self, image_data: PILImage.Image) -> PILImage.Image:
        """Применить фильтр и вернуть результат."""
        raise NotImplementedError


class BrightnessFilter(ImageFilter):
    """Изменение яркости изображения."""

    def __init__(self, factor: float = 1.5) -> None:
        if factor < 0:
            raise ValueError("Коэффициент яркости не может быть отрицательным")

        self.factor = factor

    def apply(self, image_data: PILImage.Image) -> PILImage.Image:
        """Вернуть новое изображение с изменённой яркостью."""
        return ImageEnhance.Brightness(image_data).enhance(self.factor)


class ContrastFilter(ImageFilter):
    """Изменение контраста изображения."""

    def __init__(self, factor: float = 1.5) -> None:
        if factor < 0:
            raise ValueError("Коэффициент контраста не может быть отрицательным")

        self.factor = factor

    def apply(self, image_data: PILImage.Image) -> PILImage.Image:
        """Вернуть новое изображение с изменённым контрастом."""
        return ImageEnhance.Contrast(image_data).enhance(self.factor)


class BlurFilter(ImageFilter):
    """Размытие изображения."""

    def __init__(self, radius: float = 2.0) -> None:
        if radius < 0:
            raise ValueError("Радиус размытия не может быть отрицательным")

        self.radius = radius

    def apply(self, image_data: PILImage.Image) -> PILImage.Image:
        """Вернуть новое размытое изображение."""
        return image_data.filter(PILImageFilter.GaussianBlur(radius=self.radius))


def process_image(image_data: PILImage.Image, filters: list[ImageFilter]) -> PILImage.Image:
    """Последовательно применить переданные фильтры."""
    result = image_data

    for filter_obj in filters:
        result = filter_obj.apply(result)

    return result
