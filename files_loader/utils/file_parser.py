from typing import Dict, List, Callable
from langchain_core.documents import Document


def _load_single_file(file_path: str, loader_func: Callable[[str, bool], List[Document]], keep_layout: bool) -> List[Document]:
    """Загружает один файл с помощью переданной функции загрузки."""
    return loader_func(file_path, keep_layout)


def load_files(data: Dict[str, Callable[[str, bool], List[Document]]], keep_layout: bool) -> Dict[str, List[Document]]:
    """Загружает файлы, используя предоставленные функции загрузки."""
    results = {}
    for file_path, loader_func in data.items():
        try:
            documents = _load_single_file(file_path, loader_func, keep_layout)
            results[file_path] = documents
        except:
            pass
    return results