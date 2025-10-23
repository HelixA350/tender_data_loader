from typing import List, Callable, Dict
import os
from ..loaders import load_excel, load_pdf, load_word, load_undefined
from langchain_core.documents import Document

def get_file_extension(file_path: str) -> str:
    """Возвращает расширение файла в нижнем регистре без точки."""
    _, ext = os.path.splitext(file_path)
    return ext.lower().lstrip('.')


def get_processor_by_extension(extension: str) -> Callable[[str, bool], List[Document]]:
    """Возвращает обработчик по расширению файла."""
    extension_map = {
        # PDF
        'pdf': load_pdf,
        # Word
        'doc': load_word,
        'docx': load_word,
        'rtf': load_word,
        'odt': load_word,
        # Excel
        'xls': load_excel,
        'xlsx': load_excel,
        'xlsm': load_excel,
        'ods': load_excel,
        # Другие текстовые/документные форматы (по умолчанию — undefined)
    }
    return extension_map.get(extension, load_undefined)


def map_file_to_processor(file_path: str) -> Callable[[str, bool], List[Document]]:
    """Определяет обработчик для файла по его расширению."""
    ext = get_file_extension(file_path)
    return get_processor_by_extension(ext)


def choose_processor(file_paths: List[str]) -> Dict[str, Callable[[str, bool],  List[Document]]]:
    """Сопоставляет каждому пути файлу функцию-обработчик по расширению."""
    return {
        file_path: map_file_to_processor(file_path)
        for file_path in file_paths
    }