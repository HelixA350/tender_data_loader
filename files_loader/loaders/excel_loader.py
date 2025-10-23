from typing import List, Dict, Any
import pandas as pd
from langchain_core.documents import Document
import os


def _read_excel_sheets(file_path: str) -> Dict[str, pd.DataFrame]:
    """Читает все листы Excel-файла в словарь датафреймов."""
    return pd.read_excel(file_path, sheet_name=None)


def _convert_sheet_to_text(df: pd.DataFrame, keep_layout: bool) -> str:
    """Преобразует датафрейм в текстовое представление с учётом флага сохранения структуры."""
    if keep_layout:
        # Сохраняем структуру как таблицу в текстовом виде
        return df.to_string(index=False)
    else:
        # Просто объединяем все ячейки в одну строку через пробелы
        return " ".join(df.astype(str).values.flatten())


def _create_documents_from_sheets(
    sheets: Dict[str, pd.DataFrame], keep_layout: bool
) -> List[Document]:
    """Создаёт список Document из словаря листов."""
    documents = []
    for sheet_name, df in sheets.items():
        content = _convert_sheet_to_text(df, keep_layout)
        metadata = {"source": sheet_name}
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

def modify_dir(file_path: str) -> str:
    """Совмещает имя файла с путем к корневой директории, обрабатываемых файлов"""
    root = os.getenv("ROOT")
    file_path = os.path.join(root, file_path)

    return file_path

def load_excel(file_path: str, keep_layout: bool) -> List[Document]:
    """Загружает Excel-файл и возвращает список документов langchain."""
    # Совмещаем с путем к корневой директории, обрабатываемых файлов
    file_path = modify_dir(file_path)

    sheets = _read_excel_sheets(file_path)
    return _create_documents_from_sheets(sheets, keep_layout)