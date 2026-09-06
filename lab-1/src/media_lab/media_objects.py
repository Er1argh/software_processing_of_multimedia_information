class MediaObject:
    """Базовый класс для мультимедийного объекта."""

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

    def __init__(self, filename: str, width: int = 0, height: int = 0) -> None:
        super().__init__(filename, 0)

        if width < 0 or height < 0:
            raise ValueError("Ширина и высота не могут быть отрицательными")

        self.width = width
        self.height = height

    def get_resolution(self) -> str:
        """Вернуть разрешение изображения в формате "ШИРИНАxВЫСОТА"."""
        return f"{self.width}x{self.height}"

    def get_info(self) -> str:
        """Вернуть расширенную информацию об изображении."""
        return (
            f"{super().get_info()}, "
            f"{self.get_resolution()}"
        )
