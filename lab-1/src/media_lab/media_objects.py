"""Классы мультимедийных объектов"""

from pathlib import Path
from typing import Any

from PIL import Image as PILImage
from PIL.ExifTags import TAGS


class MediaObject:
    """Базовый класс для всех мультимедийных объектов."""

    def __init__(self, filename: str, duration: float = 0.0) -> None:
        if not isinstance(filename, str):
            raise TypeError("Имя файла должно быть строкой")

        if not filename.strip():
            raise ValueError("Имя файла не может быть пустым")

        if duration < 0:
            raise ValueError("Длительность не может быть отрицательной")

        self.filename = filename
        self.duration = duration

    def get_info(self) -> str:
        """Вернуть основную информацию об объекте."""
        return f"{self.filename}: {self.duration:g} сек"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.filename})>"


class Image(MediaObject):
    """Изображение с базовыми параметрами и EXIF-метаданными."""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self, filename: str, width: int = 0, height: int = 0, exif_data: dict[str, Any] | None = None) -> None:
        super().__init__(filename, duration=0.0)

        if width < 0 or height < 0:
            raise ValueError("Ширина и высота не могут быть отрицательными")

        self.width = width
        self.height = height
        self.exif_data: dict[str, Any] = dict(exif_data or {})
        self.date_taken = self.exif_data.get("DateTimeOriginal") or self.exif_data.get("DateTime")
        self.camera = self._build_camera_info(self.exif_data)
        self.color_space: str = "unknown"

    @classmethod
    def from_file(cls, image_path: str | Path) -> "Image":
        """Создать объект Image, прочитав размер, цветовой режим и EXIF из файла."""
        path = Path(image_path)

        if not path.is_file():
            raise FileNotFoundError(f"Файл не найден: {path}")

        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Неподдерживаемый формат {path.suffix!r}; "
                f"ожидался JPG, JPEG или PNG"
            )

        with PILImage.open(path) as image:
            exif = image.getexif()
            exif_data = {
                TAGS.get(tag, f"Unknown Tag {tag}"): value for tag, value in exif.items()
            }
            result = cls(
                filename=str(path),
                width=image.width,
                height=image.height,
                exif_data=exif_data,
            )
            result.color_space = image.mode

            return result

    def get_resolution(self) -> str:
        """Вернуть разрешение изображения в формате «ШИРИНАxВЫСОТА»."""
        return f"{self.width}x{self.height}"

    def get_color_space(self) -> str:
        """Вернуть цветовой режим Pillow, например RGB или L."""
        return self.color_space

    @staticmethod
    def _build_camera_info(exif_data: dict[str, Any]) -> str:
        """Сформировать строку с производителем и моделью камеры."""
        make = exif_data.get("Make")
        model = exif_data.get("Model")

        if make and model:
            return f"{make} {model}"

        if model:
            return str(model)

        if make:
            return str(make)

        return "Информация о камере отсутствует"

    def get_exif_data(self) -> dict[str, Any]:
        """Вернуть копию EXIF-метаданных."""
        return dict(self.exif_data)

    def get_camera_info(self) -> str:
        """Вернуть информацию о производителе и модели камеры из EXIF."""
        return self.camera

    def get_info(self) -> str:
        """Вернуть расширенную информацию об изображении."""
        return (
            f"{super().get_info()}, "
            f"разрешение={self.get_resolution()}, "
            f"цветовой режим={self.get_color_space()}, "
            f"камера={self.get_camera_info()}"
        )


class MediaLibrary:
    """Коллекция мультимедийных объектов."""

    def __init__(self) -> None:
        self.media_objects: list[MediaObject] = []

    def add(self, media_obj: MediaObject) -> None:
        """Добавить объект в библиотеку."""
        if not isinstance(media_obj, MediaObject):
            raise TypeError("В библиотеку можно добавлять только MediaObject")

        self.media_objects.append(media_obj)

    def get_total_duration(self) -> float:
        """Вернуть суммарную длительность всех объектов."""
        return sum(obj.duration for obj in self.media_objects)

    def filter_by_type(self, media_type: type[MediaObject]) -> list[MediaObject]:
        """Вернуть объекты заданного типа или его наследников."""
        return [obj for obj in self.media_objects if isinstance(obj, media_type)]
