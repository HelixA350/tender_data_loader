from files_loader import Loader
from pprint import pprint
from typing import Dict, List
from langchain_core.documents import Document  # или from langchain.schema import Document

def print_document_dict_stats(doc_dict: Dict[str, List[Document]]) -> None:
    if not doc_dict:
        print("Словарь пуст.")
        return

    num_keys = len(doc_dict)
    total_docs = sum(len(docs) for docs in doc_dict.values())
    docs_per_key = [len(docs) for docs in doc_dict.values()]
    avg_docs = total_docs / num_keys
    min_docs = min(docs_per_key)
    max_docs = max(docs_per_key)

    # Собираем статистику по длине текста (в символах)
    all_texts = [doc.page_content for docs in doc_dict.values() for doc in docs]
    text_lengths = [len(text) for text in all_texts]
    total_chars = sum(text_lengths)
    avg_chars = total_chars / len(text_lengths) if text_lengths else 0
    min_chars = min(text_lengths) if text_lengths else 0
    max_chars = max(text_lengths) if text_lengths else 0

    # Вывод
    print("=== Статистика по словарю документов ===")
    print(f"Количество ключей (групп): {num_keys}")
    print(f"Общее количество документов: {total_docs}")
    print(f"Документов на ключ — среднее: {avg_docs:.2f}, мин: {min_docs}, макс: {max_docs}")
    print(f"Общее количество символов: {total_chars}")
    print(f"Средняя длина документа (символы): {avg_chars:.2f}")
    print(f"Мин. длина документа: {min_chars}")
    print(f"Макс. длина документа: {max_chars}")

    # Опционально: показать примеры ключей и количества документов
    print("\nПримеры ключей и количества документов:")
    for i, (key, docs) in enumerate(doc_dict.items()):
        print(f"  {key}: {len(docs)} документов")
    if num_keys > 5:
        print("  ...")

if __name__ == '__main__':
    path = r'C:\Users\Aleksandr\Downloads\files\files\73_2'
    loader = Loader(path, keep_layout=False)
    res = loader.load_from_directory()
    print_document_dict_stats(res)

    