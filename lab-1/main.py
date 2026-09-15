"""Демонстрация работы"""

from pathlib import Path

from PIL import Image as PILImage

from media_lab.filters import (
    BlurFilter,
    BrightnessFilter,
    ContrastFilter,
    process_image,
)
from media_lab.media_objects import (
    Image,
    MediaLibrary,
)

ROOT = Path(__file__).resolve().parent
SAMPLE_IMAGE = ROOT / "data" / "sample.jpg"
OUTPUT_IMAGE = ROOT / "output" / "filtered.jpg"


def main() -> None:
    image = Image.from_file(SAMPLE_IMAGE)

    print("=== Медиаобъект ===")
    print(image)
    print(image.get_info())
    print(f"Разрешение: {image.get_resolution()}")
    print(f"Цветовой режим: {image.get_color_space()}")
    print(f"Камера: {image.get_camera_info()}")
    print("EXIF:")

    for tag, value in image.get_exif_data().items():
        print(f"  {tag}: {value}")

    library = MediaLibrary()
    library.add(image)

    print("\n=== MediaLibrary ===")
    print(f"Количество объектов: {len(library.media_objects)}")
    print(f"Общая длительность: {library.get_total_duration():g} сек")
    print(f"Количество изображений: {len(library.filter_by_type(Image))}")

    with PILImage.open(SAMPLE_IMAGE) as source:
        filters = [BrightnessFilter(1.15), ContrastFilter(1.2), BlurFilter(4)]
        result = process_image(source, filters)
        result.save(OUTPUT_IMAGE, format="JPEG", quality=95)


    print(f"\nРезультат фильтрации сохранён: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
