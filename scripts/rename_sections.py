#!/usr/bin/env python3
"""Быстрое переименование section-NN.md файлов на основе их содержимого"""

import re
from pathlib import Path


def slugify(text: str) -> str:
    """Создать slug из текста"""
    text = re.sub(r"\*+", "", text)  # Убрать звездочки
    text = re.sub(r"^\d+\.\s+", "", text)  # Убрать номера
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.lower().strip("-")


def extract_heading(content: str) -> str | None:
    """Извлечь первый заголовок"""
    for pattern in [r"^#\s+(.+)$", r"^##\s+(.+)$", r"^###\s+(.+)$", r"^####\s+(.+)$"]:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def main():
    docs_dir = Path(__file__).parent.parent / "docs" / "r2r"
    section_files = sorted(docs_dir.glob("section-*.md"))

    print(f"\nНайдено {len(section_files)} файлов для переименования\n")

    renamed = 0
    for file_path in section_files:
        content = file_path.read_text(encoding="utf-8")
        heading = extract_heading(content)

        if not heading:
            print(f"⊘ {file_path.name} - заголовок не найден")
            continue

        slug = slugify(heading)
        new_name = f"{slug}.md"
        new_path = file_path.parent / new_name

        if new_path.exists() and new_path != file_path:
            # Добавляем суффикс если файл уже существует
            counter = 2
            while (file_path.parent / f"{slug}-{counter}.md").exists():
                counter += 1
            new_name = f"{slug}-{counter}.md"
            new_path = file_path.parent / new_name

        file_path.rename(new_path)
        print(f"✓ {file_path.name:30s} -> {new_name}")
        renamed += 1

    print(f"\n✅ Переименовано: {renamed} файлов\n")


if __name__ == "__main__":
    main()
