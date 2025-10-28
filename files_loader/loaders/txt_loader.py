from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
import os


def _create_txt_loader(file_path: str) -> TextLoader:
    """
    Создаёт загрузчик текстового файла.
    Для .txt файлов стратегия обработки не требуется — используется простой TextLoader.
    """
    return TextLoader(file_path, encoding="utf-8")


def _load_txt_documents(loader: TextLoader) -> List[Document]:
    """
    Загружает документы с помощью переданного загрузчика текстового файла.
    """
    return loader.load()


def modify_dir(file_path: str) -> str:
    """Совмещает имя файла с путем к корневой директории обрабатываемых файлов."""
    root = os.getenv("ROOT")
    file_path = os.path.join(root, file_path)
    return file_path


def load_txt(file_path: str) -> List[Document]:
    """
    Извлекает содержимое текстового (.txt) файла в виде списка документов LangChain.
    """
    file_path = modify_dir(file_path)
    loader = _create_txt_loader(file_path)
    documents = _load_txt_documents(loader)
    return documents