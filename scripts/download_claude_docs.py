#!/usr/bin/env python3
"""
Скрипт для загрузки документации Claude Code из llms.txt

Загружает все markdown файлы документации и сохраняет их в docs/claude_code/
"""

import logging
import re
import sys
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Ошибка: требуются библиотеки requests и tqdm")
    print("Установите их: pip install requests tqdm")
    sys.exit(1)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("download_claude_docs.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ClaudeDocsDownloader:
    """Загрузчик документации Claude Code"""

    def __init__(
        self,
        llms_txt_url: str = "https://code.claude.com/docs/llms.txt",
        output_dir: str = "docs/claude_code",
    ):
        self.llms_txt_url = llms_txt_url
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            }
        )
        self.stats = {"success": 0, "failed": 0, "skipped": 0}

    def fetch_llms_txt(self) -> str:
        """Загрузить содержимое файла llms.txt"""
        logger.info(f"Загрузка llms.txt из {self.llms_txt_url}")
        try:
            response = self.session.get(self.llms_txt_url, timeout=30)
            response.raise_for_status()
            logger.info("llms.txt успешно загружен")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Ошибка загрузки llms.txt: {e}")
            raise

    def parse_markdown_urls(self, content: str) -> List[str]:
        """
        Извлечь все URL markdown файлов из llms.txt

        Ожидаемый формат: - [Title](URL): Description
        """
        # Паттерн для извлечения URL из markdown ссылок
        pattern = r"\[([^\]]+)\]\((https://code\.claude\.com/docs/[^\)]+\.md)\)"
        matches = re.findall(pattern, content)
        urls = [url for _, url in matches]
        logger.info(f"Найдено {len(urls)} markdown файлов для загрузки")
        return urls

    def get_local_path(self, url: str) -> Path:
        """
        Получить локальный путь для сохранения файла

        Пример: https://code.claude.com/docs/en/setup.md -> docs/claude_code/setup.md
        """
        parsed = urlparse(url)
        # Убираем /docs/en/ из пути и оставляем только имя файла и подпапки
        path_parts = parsed.path.split("/")
        # Находим индекс 'en' и берем все после него
        try:
            en_index = path_parts.index("en")
            relative_path = "/".join(path_parts[en_index + 1 :])
        except ValueError:
            # Если 'en' не найдено, берем имя файла
            relative_path = path_parts[-1]

        return self.output_dir / relative_path

    def download_file(
        self, url: str, local_path: Path, overwrite: bool = False
    ) -> bool:
        """
        Загрузить один файл

        Args:
            url: URL файла для загрузки
            local_path: Локальный путь для сохранения
            overwrite: Перезаписывать существующие файлы

        Returns:
            True если успешно, False если ошибка
        """
        # Проверка существования файла
        if local_path.exists() and not overwrite:
            logger.info(f"Файл уже существует, пропускаем: {local_path.name}")
            self.stats["skipped"] += 1
            return True

        # Создание директории если нужно
        local_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.debug(f"Загрузка {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Сохранение файла
            local_path.write_text(response.text, encoding="utf-8")
            logger.info(f"✓ Сохранен: {local_path.name} ({len(response.text)} байт)")
            self.stats["success"] += 1
            return True

        except requests.RequestException as e:
            logger.error(f"✗ Ошибка загрузки {url}: {e}")
            self.stats["failed"] += 1
            return False
        except Exception as e:
            logger.error(f"✗ Ошибка сохранения {local_path}: {e}")
            self.stats["failed"] += 1
            return False

    def download_all(self, overwrite: bool = False) -> Tuple[int, int, int]:
        """
        Загрузить все файлы документации

        Args:
            overwrite: Перезаписывать существующие файлы

        Returns:
            Кортеж (успешно, ошибок, пропущено)
        """
        # Создание выходной директории
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Выходная директория: {self.output_dir.absolute()}")

        # Загрузка и парсинг llms.txt
        content = self.fetch_llms_txt()
        urls = self.parse_markdown_urls(content)

        if not urls:
            logger.error("Не найдено ни одного URL для загрузки")
            return (0, 0, 0)

        # Загрузка всех файлов с прогресс-баром
        logger.info(f"\nНачало загрузки {len(urls)} файлов...\n")

        with tqdm(total=len(urls), desc="Загрузка документации", unit="файл") as pbar:
            for url in urls:
                local_path = self.get_local_path(url)
                self.download_file(url, local_path, overwrite)
                pbar.update(1)

        # Создание README
        self.create_readme(urls)

        return (self.stats["success"], self.stats["failed"], self.stats["skipped"])

    def create_readme(self, urls: List[str]) -> None:
        """Создать README.md с информацией о загруженных файлах"""
        readme_path = self.output_dir / "README.md"

        readme_content = f"""# Claude Code Documentation

Автоматически загружено из {self.llms_txt_url}

## Статистика

- Всего файлов: {len(urls)}
- Успешно загружено: {self.stats['success']}
- Пропущено (уже существуют): {self.stats['skipped']}
- Ошибок: {self.stats['failed']}

## Структура

```
claude_code/
"""

        # Добавление списка файлов
        for url in sorted(urls):
            local_path = self.get_local_path(url)
            relative = local_path.relative_to(self.output_dir)
            readme_content += f"├── {relative}\n"

        readme_content += """```

## Использование

Эти файлы являются официальной документацией Claude Code.
Для получения последней версии документации запустите скрипт повторно с флагом `--overwrite`.

## Источник

- Основной сайт: https://code.claude.com/
- Список документов: https://code.claude.com/docs/llms.txt
"""

        readme_path.write_text(readme_content, encoding="utf-8")
        logger.info(f"Создан README.md: {readme_path}")


def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Загрузка документации Claude Code из llms.txt"
    )
    parser.add_argument(
        "--output-dir",
        default="docs/claude_code",
        help="Директория для сохранения файлов (по умолчанию: docs/claude_code)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Перезаписывать существующие файлы",
    )
    parser.add_argument(
        "--url",
        default="https://code.claude.com/docs/llms.txt",
        help="URL файла llms.txt (по умолчанию: официальный URL)",
    )

    args = parser.parse_args()

    # Создание загрузчика и запуск
    downloader = ClaudeDocsDownloader(
        llms_txt_url=args.url, output_dir=args.output_dir
    )

    try:
        success, failed, skipped = downloader.download_all(overwrite=args.overwrite)

        # Вывод итоговой статистики
        print("\n" + "=" * 60)
        print("ИТОГОВАЯ СТАТИСТИКА")
        print("=" * 60)
        print(f"✓ Успешно загружено: {success}")
        print(f"⊘ Пропущено (уже существуют): {skipped}")
        print(f"✗ Ошибок: {failed}")
        print(f"📁 Директория: {Path(args.output_dir).absolute()}")
        print("=" * 60)

        # Код возврата
        sys.exit(0 if failed == 0 else 1)

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
