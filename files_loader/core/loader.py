from typing import Dict, List
from langchain_core.documents import Document
from ..utils import extract_and_list_files, load_files, choose_processor

class Loader:
    """
    Класс для загрузки документов из указанной директории.

    Атрибуты:
        dir_path (str): Путь к директории, из которой будут загружаться файлы.
        keep_layout (bool): Флаг, указывающий, сохранять ли исходный макет документа.
    """

    def __init__(self, dir_path: str, keep_layout: bool = True):
        """
        Инициализация экземпляра класса Loader.

        Args:
            dir_path: Путь к директории с файлами.
            keep_layout: Флаг, определяющий, нужно ли сохранять исходный макет документа.
                Позволяет сохранить табличную структуру, разделение на абзацы и т.д.
        """
        self.dir_path = dir_path
        self.keep_layout = keep_layout

    def load_from_directory(self) -> Dict[str, List[Document]]:
        """
        Загружает и обрабатывает документы из указанной директории.

        Returns:
            Словарь, где ключ — имя файла, значение — список извлеченных 
            langchain Document из этого файла.
        
        Calls:
            extract_and_list_files: Распаковывает архивы и составляет список путей к файлам.
            choose_processor: Выбирает подходящий процессор для обработки каждого файла.
            load_files: Загружает файлы с использованием выбранного процессора.
        """
        file_paths = extract_and_list_files(self.dir_path)
        processing_data = choose_processor(file_paths)
        return processing_data

        # return load_files(processing_data, self.keep_layout)