"""Тесты"""
from PIL import Image as PILImage
from pytest import raises

from media_lab.filters import (
    BlurFilter,
    BrightnessFilter,
    ContrastFilter,
    ImageFilter,
    process_image,
)
from media_lab.media_objects import (
    Image,
    MediaLibrary,
    MediaObject,
)


def test_media_object_get_info() -> None:
    """Проверить формирование базовой информации."""
    media = MediaObject("movie.mp4", 120)

    assert media.get_info() == "movie.mp4: 120 сек"


def test_media_object_str() -> None:
    """Проверить строковое представление объекта."""
    media = MediaObject("movie.mp4", 120)

    assert str(media) == "<MediaObject(movie.mp4)>"


def test_media_object_rejects_empty_filename() -> None:
    """Проверить запрет пустого имени файла."""
    with raises(ValueError):
        MediaObject("")


def test_media_object_rejects_negative_duration() -> None:
    """Проверить запрет отрицательной длительности."""
    with raises(ValueError):
        MediaObject("movie.mp4", -1)


def test_media_object_rejects_invalid_filename_type() -> None:
    """Проверить тип имени файла."""
    with raises(TypeError):
        MediaObject(123)


def test_image_resolution() -> None:
    """Проверить получение разрешения."""
    image = Image("photo.jpg", 1920, 1080)

    assert image.get_resolution() == "1920x1080"


def test_image_is_media_object() -> None:
    """Image должен быть MediaObject."""
    image = Image("photo.jpg", 1920, 1080)

    assert isinstance(image, MediaObject)


def test_image_get_info() -> None:
    """Проверить расширенную информацию изображения."""
    image = Image("photo.jpg", 1920, 1080)

    assert image.get_info() == (
        "photo.jpg: 0 сек, "
        "разрешение=1920x1080, "
        "цветовой режим=unknown, "
        "камера=Информация о камере отсутствует"
    )


def test_media_library_add_and_filter() -> None:
    """Проверить добавление объектов и фильтрацию."""
    library = MediaLibrary()

    image_1 = Image("one.jpg", 100, 100)
    image_2 = Image("two.jpg", 200, 200)

    library.add(image_1)
    library.add(image_2)

    assert len(library.media_objects) == 2
    assert library.filter_by_type(Image) == [image_1, image_2]


def test_filters_implement_common_interface() -> None:
    """Все конкретные фильтры должны быть ImageFilter."""
    assert isinstance(BrightnessFilter(), ImageFilter)
    assert isinstance(ContrastFilter(), ImageFilter)
    assert isinstance(BlurFilter(), ImageFilter)


def test_image_filter_is_abstract() -> None:
    """Нельзя создать абстрактный ImageFilter."""
    with raises(TypeError):
        ImageFilter()


def test_process_image() -> None:
    """Проверить последовательное применение фильтров."""
    image = PILImage.new("RGB", (10, 10), color="white")

    filters = [
        BrightnessFilter(1.0),
        ContrastFilter(1.0),
        BlurFilter(3),
    ]

    result = process_image(image, filters)

    assert result.size == (10, 10)
