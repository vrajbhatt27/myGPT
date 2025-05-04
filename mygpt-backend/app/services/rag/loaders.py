# mygpt-backend/app/services/rag/loaders.py

from io import BytesIO

import fitz  # PyMuPDF


def extract_text_from_pdf(file: BytesIO) -> str:
    """
    Extracts raw text from all pages of a PDF file.

    Args:
        file (BytesIO): The uploaded PDF file in memory.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""

    try:
        # Open in-memory PDF
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text()
                text += f"\n--- Page {page_num} ---\n{page_text}"

    except Exception as e:
        raise RuntimeError(f"Error while extracting PDF text: {str(e)}")

    return text.strip()
