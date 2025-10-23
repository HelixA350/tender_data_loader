from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os


def _create_loader(file_path: str, keep_layout: bool) -> UnstructuredWordDocumentLoader:
    """
    Создаёт загрузчик Word-документа с учётом флага сохранения структуры.
    """
    strategy = "hi_res" if keep_layout else "fast"
    return UnstructuredWordDocumentLoader(file_path, mode="elements", strategy=strategy)


def _load_documents(loader: UnstructuredWordDocumentLoader) -> List[Document]:
    """
    Загружает документы с помощью переданного загрузчика.
    """
    return loader.load()

def modify_dir(file_path: str) -> str:
    """Совмещает имя файла с путем к корневой директории, обрабатываемых файлов"""
    root = os.getenv("ROOT")
    file_path = os.path.join(root, file_path)

    return file_path


def load_word(file_path: str, keep_layout: bool) -> List[Document]:
    """
    Извлекает содержимое Word-файла в виде списка документов LangChain.
    """
    file_path = modify_dir(file_path)
    loader = _create_loader(file_path, keep_layout)
    documents = _load_documents(loader)


    print(len(documents))
    return documents