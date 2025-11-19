#!/usr/bin/env python3
"""
Скрипт для разделения документации R2R из llms.txt на отдельные файлы

Читает файл docs/llms.txt, разделяет его по заголовкам уровня 2 (##)
и сохраняет каждую часть в отдельный файл с осмысленным именем.
"""

import re
from pathlib import Path
from typing import List, Tuple


def slugify(text: str) -> str:
    """
    Создать URL-friendly slug из текста

    Args:
        text: Исходный текст

    Returns:
        Slug в lowercase с дефисами вместо пробелов
    """
    # Удаляем специальные символы, оставляем только буквы, цифры, пробелы
    text = re.sub(r"[^\w\s-]", "", text)
    # Заменяем пробелы и множественные дефисы на одиночный дефис
    text = re.sub(r"[-\s]+", "-", text)
    # Lowercase и удаляем дефисы в начале/конце
    return text.lower().strip("-")


def extract_first_heading(content: str) -> str | None:
    """
    Извлечь первый заголовок уровня 2 (##) из содержимого

    Args:
        content: Markdown контент

    Returns:
        Текст заголовка или None если не найден
    """
    # Поиск первого заголовка уровня 2
    match = re.search(r"^##\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def split_document(file_path: Path) -> List[Tuple[str, str]]:
    """
    Разделить документ на части по заголовкам уровня 2 (##)

    Args:
        file_path: Путь к исходному файлу

    Returns:
        Список кортежей (заголовок, содержимое)
    """
    content = file_path.read_text(encoding="utf-8")

    # Находим все позиции заголовков уровня 2
    pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))

    if not matches:
        # Если нет заголовков уровня 2, возвращаем весь документ
        heading = extract_first_heading(content) or "Document"
        return [(heading, content)]

    result = []

    for i, match in enumerate(matches):
        # Заголовок - это текст после ##
        heading = match.group(1).strip()

        # Начало части - позиция текущего заголовка
        start = match.start()

        # Конец части - начало следующего заголовка или конец документа
        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(content)

        # Извлекаем содержимое части
        part = content[start:end].strip()

        if part:
            result.append((heading, part))

    return result


def save_parts(parts: List[Tuple[str, str]], output_dir: Path) -> None:
    """
    Сохранить части документа в отдельные файлы

    Args:
        parts: Список кортежей (заголовок, содержимое)
        output_dir: Директория для сохранения файлов
    """
    # Создание выходной директории
    output_dir.mkdir(parents=True, exist_ok=True)

    # Статистика
    total = len(parts)
    saved = 0
    skipped = 0

    print(f"\n{'='*60}")
    print(f"РАЗДЕЛЕНИЕ ДОКУМЕНТА R2R")
    print(f"{'='*60}\n")
    print(f"Всего частей: {total}")
    print(f"Выходная директория: {output_dir.absolute()}\n")

    # Счетчик для дубликатов имен файлов
    filename_counts = {}

    # Сохранение каждой части
    for i, (heading, content) in enumerate(parts, start=1):
        # Создание имени файла
        slug = slugify(heading)

        # Обработка дубликатов
        if slug in filename_counts:
            filename_counts[slug] += 1
            filename = f"{slug}-{filename_counts[slug]}.md"
        else:
            filename_counts[slug] = 0
            filename = f"{slug}.md"

        file_path = output_dir / filename

        # Сохранение
        file_path.write_text(content, encoding="utf-8")

        # Статистика
        size = len(content)
        print(f"  ✓ {filename:50s} ({size:>6d} байт) - {heading}")
        saved += 1

    print(f"\n{'='*60}")
    print(f"ИТОГОВАЯ СТАТИСТИКА")
    print(f"{'='*60}")
    print(f"✓ Сохранено файлов: {saved}")
    print(f"⊘ Пропущено: {skipped}")
    print(f"📁 Директория: {output_dir.absolute()}")
    print(f"{'='*60}\n")


def create_index(parts: List[Tuple[str, str]], output_dir: Path) -> None:
    """
    Создать индексный файл со списком всех частей

    Args:
        parts: Список кортежей (заголовок, содержимое)
        output_dir: Директория с файлами
    """
    index_path = output_dir / "README.md"

    index_content = f"""# R2R Documentation - Split Files

Документация R2R, разделенная на отдельные файлы для удобной работы.

## Статистика

- Всего файлов: {len(parts)}
- Источник: `docs/llms.txt`
- Дата разделения: автоматически

## Оглавление

"""

    # Счетчик для дубликатов имен файлов (синхронизирован с save_parts)
    filename_counts = {}

    # Добавление списка файлов
    for i, (heading, content) in enumerate(parts, start=1):
        slug = slugify(heading)

        # Обработка дубликатов (как в save_parts)
        if slug in filename_counts:
            filename_counts[slug] += 1
            filename = f"{slug}-{filename_counts[slug]}.md"
        else:
            filename_counts[slug] = 0
            filename = f"{slug}.md"

        lines = content.count("\n") + 1
        size = len(content)
        index_content += f"{i}. [{heading}]({filename}) - {lines} строк, {size} байт\n"

    index_content += """
## Использование

Каждый файл содержит отдельную секцию документации R2R.
Файлы названы по содержимому для удобной навигации.

## Источник

Оригинальный файл: `docs/llms.txt`
Скрипт разделения: `scripts/split_r2r_docs.py`
"""

    index_path.write_text(index_content, encoding="utf-8")
    print(f"Создан индексный файл: {index_path}")


def main():
    """Главная функция"""
    # Пути (скрипт находится в scripts/, корень проекта - на уровень выше)
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / "docs" / "llms.txt"
    output_dir = base_dir / "docs" / "r2r"

    # Проверка существования входного файла
    if not input_file.exists():
        print(f"❌ Ошибка: файл не найден - {input_file}")
        return 1

    print(f"Чтение файла: {input_file}")

    # Разделение документа
    parts = split_document(input_file)

    # Сохранение частей
    save_parts(parts, output_dir)

    # Создание индекса
    create_index(parts, output_dir)

    print("✅ Разделение документа завершено успешно!")
    return 0


if __name__ == "__main__":
    exit(main())
