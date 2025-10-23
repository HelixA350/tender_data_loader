from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PDFPlumberLoader
from PIL import Image
import pytesseract
import tempfile
import os


def _is_text_based_pdf(file_path: str) -> bool:
    """
    Проверяет, является ли PDF текстовым или сканированным.
    """
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        # Если хотя бы на одной странице есть текст, считаем PDF текстовым
        return any(page.page_content.strip() != "" for page in pages)
    except Exception:
        # В случае ошибки пробуем другой метод
        return False


def _extract_text_with_ocr(file_path: str) -> str:
    """
    Извлекает текст из PDF с помощью OCR.
    """
    text = ""
    try:
        # Используем PDFPlumberLoader для извлечения изображений и текста
        loader = PDFPlumberLoader(file_path)
        pages = loader.load()

        # Если текст уже извлечен, возвращаем его
        full_text = "".join(page.page_content for page in pages if page.page_content)
        if full_text.strip():
            return full_text

        # Если текст не извлечен, пробуем OCR для каждой страницы как изображения
        import fitz  # PyMuPDF

        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Попробовать получить текст напрямую
            text_from_page = page.get_text()
            if text_from_page.strip():
                text += text_from_page + "\n"
            else:
                # Если текста нет, конвертируем страницу в изображение и применяем OCR
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
                    tmp_img.write(img_data)
                    img = Image.open(tmp_img.name)
                    page_text = pytesseract.image_to_string(img, lang='rus+eng')
                    text += page_text + "\n"
                os.unlink(tmp_img.name)
        doc.close()
    except Exception:
        # Если все способы не сработали, возвращаем пустую строку
        pass
    return text


def _create_documents_from_text(text: str, file_path: str) -> List[Document]:
    """
    Создает список документов LangChain из текста.
    """
    if not text.strip():
        return []
    # Просто создаем один документ из всего текста
    return [Document(page_content=text, metadata={"source": file_path})]

def modify_dir(file_path: str) -> str:
    """Совмещает имя файла с путем к корневой директории, обрабатываемых файлов"""
    root = os.getenv("ROOT")
    file_path = os.path.join(root, file_path)

    return file_path

def load_pdf(file_path: str, keep_layout: bool) -> List[Document]:
    """
    Загружает PDF файл и возвращает список документов LangChain.
    Обрабатывает как текстовые PDF, так и сканированные (с OCR).
    """
    file_path = modify_dir(file_path)
    
    if _is_text_based_pdf(file_path):
        # Используем PDFPlumberLoader для текстовых PDF
        loader = PDFPlumberLoader(file_path)
        documents = loader.load()
    else:
        # Для сканированных PDF используем OCR
        text = _extract_text_with_ocr(file_path)
        documents = _create_documents_from_text(text, file_path)

    return documents