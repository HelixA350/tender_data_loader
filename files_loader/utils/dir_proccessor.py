import os
import zipfile
import tarfile
import rarfile
import py7zr
from pathlib import Path
from typing import List

def extract_and_list_files(directory : str) -> List[str]:
    """
    Раскрывает все архивы в директории и возвращает список полных путей всех файлов.
    
    Args:
        directory (str): Путь к корневой директории
        
    Returns:
        list[str]: Список полных путей ко всем файлам
    """
    all_files = []
    
    def process_directory(current_dir, base_path=""):
        """
        Рекурсивно обрабатывает директорию, извлекает архивы и собирает файлы.
        
        Args:
            current_dir (str): Текущая обрабатываемая директория
            base_path (str): Базовый путь для формирования полных имен файлов
        """
        try:
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                relative_path = os.path.join(base_path, item) if base_path else item
                
                if os.path.isfile(item_path):
                    # Проверяем, является ли файл архивом
                    if is_archive_file(item_path):
                        # Создаем временную директорию для извлечения
                        temp_dir = os.path.join(current_dir, f"_extracted_{item}")
                        try:
                            extract_archive(item_path, temp_dir)
                            # Рекурсивно обрабатываем извлеченную директорию
                            process_directory(temp_dir, relative_path)
                        except Exception as e:
                            print(f"Ошибка при извлечении архива {item_path}: {e}")
                    else:
                        # Обычный файл - добавляем в список
                        all_files.append(relative_path)
                elif os.path.isdir(item_path):
                    # Рекурсивно обрабатываем поддиректорию
                    process_directory(item_path, relative_path)
                    
        except PermissionError:
            print(f"Нет доступа к директории: {current_dir}")
        except Exception as e:
            print(f"Ошибка при обработке директории {current_dir}: {e}")
    
    def is_archive_file(file_path):
        """Проверяет, является ли файл архивом по расширению."""
        archive_extensions = {'.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z', 
                             '.tar.gz', '.tar.bz2', '.tar.xz'}
        return any(file_path.lower().endswith(ext) for ext in archive_extensions)
    
    def extract_archive(archive_path, extract_dir):
        """Извлекает архив в указанную директорию."""
        # Создаем директорию для извлечения
        os.makedirs(extract_dir, exist_ok=True)
        
        archive_path_lower = archive_path.lower()
        
        try:
            if archive_path_lower.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                    
            elif archive_path_lower.endswith('.tar') or \
                 archive_path_lower.endswith('.tar.gz') or \
                 archive_path_lower.endswith('.tgz') or \
                 archive_path_lower.endswith('.tar.bz2') or \
                 archive_path_lower.endswith('.tbz2') or \
                 archive_path_lower.endswith('.tar.xz') or \
                 archive_path_lower.endswith('.txz'):
                
                mode = 'r'
                if archive_path_lower.endswith('.gz') or archive_path_lower.endswith('.tgz'):
                    mode = 'r:gz'
                elif archive_path_lower.endswith('.bz2') or archive_path_lower.endswith('.tbz2'):
                    mode = 'r:bz2'
                elif archive_path_lower.endswith('.xz') or archive_path_lower.endswith('.txz'):
                    mode = 'r:xz'
                
                with tarfile.open(archive_path, mode) as tar_ref:
                    tar_ref.extractall(extract_dir)
                    
            elif archive_path_lower.endswith('.rar'):
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    rar_ref.extractall(extract_dir)
                    
            elif archive_path_lower.endswith('.7z'):
                with py7zr.SevenZipFile(archive_path, 'r') as sevenz_ref:
                    sevenz_ref.extractall(extract_dir)
                    
            else:
                raise ValueError(f"Неподдерживаемый формат архива: {archive_path}")
                
            print(f"Архив {archive_path} извлечен в {extract_dir}")
            
        except Exception as e:
            # Удаляем временную директорию в случае ошибки
            import shutil
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            raise e
    
    # Запускаем обработку
    process_directory(directory)
    return all_files

# Пример использования
if __name__ == "__main__":
    # Укажите путь к вашей директории
    test_directory = "/путь/к/вашей/директории"
    
    try:
        files = extract_and_list_files(test_directory)
        print("Найденные файлы:")
        for file in files:
            print(file)
        print(f"\nВсего файлов: {len(files)}")
    except Exception as e:
        print(f"Ошибка: {e}")

