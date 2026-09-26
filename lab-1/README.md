# ЛР №1 — ООП для обработки мультимедийных данных

**Вариант: 5 — изображения с EXIF-метаданными.**

## Что реализовано

- базовый класс `MediaObject`;
- класс `Image` с размером, цветовым режимом и EXIF;
- `get_exif_data()` и `get_camera_info()`;
- `MediaLibrary` с `add()`, `get_total_duration()`, `filter_by_type()`;
- абстрактный `ImageFilter`;
- `BrightnessFilter`, `ContrastFilter`, `BlurFilter`;
- полиморфная функция `process_image()`;
- обработка ошибок через `ValueError`, `TypeError`, `FileNotFoundError`;
- тесты на `pytest`;
- проверка качества кода через `ruff`.

## Запуск через uv

Сначала убедитесь, что в системе доступен Python 3.12:

```bash
python --version
uv --version
```

Затем из корня проекта:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run python main.py
```

`uv sync` создаёт/синхронизирует `.venv`, устанавливает зависимости и фиксирует версии в `uv.lock`.
`uv run` запускает команды внутри окружения проекта, поэтому отдельный глобальный `pip install` не требуется.

После запуска демонстрации обработанное изображение появляется в `output/filtered.jpg`.

## Структура

```text
lab-1/
├── data/
│   └── sample.jpg
├── output/
├── src/
│   └── media_lab/
│       ├── __init__.py
│       ├── filters.py
│       └── media_objects.py
├── tests/
│   └── test_media.py
├── main.py
├── pyproject.toml
└── .gitignore
```

## Почему EXIF читается через Pillow

Pillow предоставляет `Image.getexif()`, после чего числовые идентификаторы тегов можно преобразовать в читаемые названия
через `PIL.ExifTags.TAGS`.

## Настройка в PyCharm

1. Откройте папку проекта `lab-1` через **File → Open**.
2. В **Settings → Project → Python Interpreter** выберите существующий интерпретатор `.venv`.
3. Если `.venv` ещё нет, сначала выполните `uv sync` в терминале PyCharm.
4. Для запуска `main.py` используйте обычную конфигурацию Python, а для тестов — конфигурацию `pytest` или команду
   `uv run pytest` в терминале.

`src`-структура специально отделяет исходный пакет от тестов и вспомогательных файлов; это уменьшает риск случайных
импортов из корня проекта.

## Почему мы не используем `pip install Pillow` напрямую

Методичка показывает `pip install Pillow`, но для современного проекта с uv практичнее объявить зависимость в
`pyproject.toml`, а затем синхронизировать окружение через `uv sync`. Это делает список зависимостей воспроизводимым и
позволяет зафиксировать конкретные версии в `uv.lock`.
