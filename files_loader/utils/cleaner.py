from langchain_core.documents import Document
from typing import Dict, List

def cleanup(processed_result: Dict[str, List[Document]]) -> Dict[str, List[Document]]:
    """Удалить пустые результаты."""
    return {key: value for key, value in processed_result.items() if value}