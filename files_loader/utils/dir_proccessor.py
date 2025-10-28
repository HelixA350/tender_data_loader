from typing import List
import os
import zipfile
import rarfile
import py7zr
import tarfile
import tempfile
import shutil


def is_archive_file(filepath: str) -> bool:
    """Проверяет, является ли файл архивом."""
    archive_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'}
    return os.path.isfile(filepath) and any(filepath.lower().endswith(ext) for ext in archive_extensions)


def extract_archive(archive_path: str, extract_to: str) -> None:
    """Извлекает архив в указанную директорию."""
    if archive_path.lower().endswith(('.tar', '.gz', '.bz2', '.xz')):
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)
    elif archive_path.lower().endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.lower().endswith('.rar'):
        #TODO:  сделать коректную распаковку rar
        with rarfile.RarFile(archive_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
    elif archive_path.lower().endswith('.7z'):
        with py7zr.SevenZipFile(archive_path, mode='r') as z:
            z.extractall(path=extract_to)


def process_directory_recursive(directory: str) -> None:
    """Рекурсивно обрабатывает директорию, распаковывая все архивы."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_archive_file(file_path):
                # Создаем директорию для извлечения
                archive_name = os.path.splitext(file)[0]
                extract_dir = os.path.join(root, archive_name)
                os.makedirs(extract_dir, exist_ok=True)
                
                # Извлекаем архив
                try:
                    extract_archive(file_path, extract_dir)
                except:
                    pass
                
                # Удаляем файл архива
                os.remove(file_path)
                
                # Рекурсивно обрабатываем извлеченную директорию
                process_directory_recursive(extract_dir)


def get_all_files_recursive(directory: str) -> List[str]:
    """Возвращает список всех файлов в директории и поддиректориях."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            file_list.append(relative_path.replace(os.sep, '\\'))
    return file_list

def save_root_to_env(root: str) -> None:
    if root:
        os.environ['ROOT'] = root
    else:
        os.environ['ROOT'] = ''
    return None

def extract_and_list_files(dir: str) -> List[str]:
    """Распаковывает все архивы в директории и возвращает список всех файлов."""
    # сохраняем корневую директорию для возможности открытия файлов
    save_root_to_env(dir)
    
    # Создаем временную директорию для работы
    with tempfile.TemporaryDirectory() as temp_dir:
        # Копируем содержимое исходной директории во временную
        temp_main_dir = os.path.join(temp_dir, 'main')
        shutil.copytree(dir, temp_main_dir)

        # Рекурсивно обрабатываем директорию, распаковывая все архивы
        process_directory_recursive(temp_main_dir)

        # Собираем список всех файлов
        all_files = get_all_files_recursive(temp_main_dir)
        
        return all_files