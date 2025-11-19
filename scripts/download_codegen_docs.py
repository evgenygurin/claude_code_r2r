#!/usr/bin/env python3
"""
Скрипт для загрузки документации Codegen из llms.txt

Извлекает все ссылки на markdown файлы и загружает их в docs/codegen/
"""

import logging
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import time

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
        logging.FileHandler("download_codegen_docs.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class CodegenDocsDownloader:
    """Загрузчик документации Codegen"""

    def __init__(
        self,
        llms_txt_path: str = "docs/codegen/llms.txt",
        output_dir: str = "docs/codegen",
    ):
        self.llms_txt_path = Path(llms_txt_path)
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

    def parse_markdown_urls(self) -> list[str]:
        """
        Извлечь все URL markdown файлов из llms.txt
        
        Формат: [Title](https://docs.codegen.com/path/file.md)
        """
        if not self.llms_txt_path.exists():
            logger.error(f"Файл не найден: {self.llms_txt_path}")
            return []
        
        content = self.llms_txt_path.read_text(encoding="utf-8")
        
        # Паттерн для извлечения URL из markdown ссылок
        pattern = r"\]\((https://docs\.codegen\.com/[^\)]+\.md)\)"
        urls = re.findall(pattern, content)
        
        # Убираем дубликаты и сортируем
        unique_urls = sorted(set(urls))
        
        logger.info(f"Найдено {len(unique_urls)} уникальных markdown файлов для загрузки")
        return unique_urls

    def get_local_path(self, url: str) -> Path:
        """
        Получить локальный путь для сохранения файла
        
        Пример: https://docs.codegen.com/api-reference/agents.md -> docs/codegen/api-reference/agents.md
        """
        parsed = urlparse(url)
        # Убираем начальный слеш и берем путь после docs.codegen.com
        path_parts = parsed.path.lstrip('/').split('/')
        relative_path = '/'.join(path_parts)
        
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
            logger.debug(f"Файл уже существует, пропускаем: {local_path}")
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
            logger.debug(f"✓ Сохранен: {local_path.relative_to(self.output_dir)} ({len(response.text)} байт)")
            self.stats["success"] += 1
            
            # Небольшая пауза чтобы не перегружать сервер
            time.sleep(0.1)
            return True

        except requests.RequestException as e:
            logger.error(f"✗ Ошибка загрузки {url}: {e}")
            self.stats["failed"] += 1
            return False
        except Exception as e:
            logger.error(f"✗ Ошибка сохранения {local_path}: {e}")
            self.stats["failed"] += 1
            return False

    def download_all(self, overwrite: bool = False) -> tuple[int, int, int]:
        """
        Загрузить все файлы документации
        
        Args:
            overwrite: Перезаписывать существующие файлы
        
        Returns:
            Кортеж (успешно, ошибок, пропущено)
        """
        # Проверка существования llms.txt
        if not self.llms_txt_path.exists():
            logger.error(f"Файл llms.txt не найден: {self.llms_txt_path}")
            return (0, 0, 0)

        # Создание выходной директории
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Выходная директория: {self.output_dir.absolute()}")

        # Парсинг URL из llms.txt
        urls = self.parse_markdown_urls()

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

        return (self.stats["success"], self.stats["failed"], self.stats["skipped"])


def main():
    """Главная функция"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Загрузка документации Codegen из llms.txt"
    )
    parser.add_argument(
        "--llms-txt",
        default="docs/codegen/llms.txt",
        help="Путь к файлу llms.txt (по умолчанию: docs/codegen/llms.txt)",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/codegen",
        help="Директория для сохранения файлов (по умолчанию: docs/codegen)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Перезаписывать существующие файлы",
    )

    args = parser.parse_args()

    # Создание загрузчика и запуск
    downloader = CodegenDocsDownloader(
        llms_txt_path=args.llms_txt, output_dir=args.output_dir
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
