# mygpt-backend/app/services/rag/loaders.py

from io import BytesIO

import fitz  # PyMuPDF
import pandas as pd


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


def extract_text_from_csv(file: BytesIO) -> str:
    """
    Reads a CSV file from memory and returns its content as readable plain text.

    Args:
        file (BytesIO): The uploaded CSV file in memory.

    Returns:
        str: Stringified CSV content.
    """
    try:
        # Read CSV using pandas
        df = pd.read_csv(file)

        # Convert the DataFrame to plain text
        # - index=False → don’t show row numbers
        # - header=True → keep column names
        return df.to_string(index=False)

    except Exception as e:
        raise RuntimeError(f"Error while reading CSV file: {str(e)}")


# mygpt-backend/app/services/rag/loaders.py


def extract_text_from_file(file: BytesIO, file_type: str) -> str:
    """
    Dispatcher to extract text from either PDF or CSV file.

    Args:
        file (BytesIO): The uploaded file in memory.
        file_type (str): Type of file, either 'pdf' or 'csv'.

    Returns:
        str: Extracted text content.
    """
    # Reset the file pointer (very important after first read)
    file.seek(0)

    if file_type == "pdf":
        return extract_text_from_pdf(file)

    elif file_type == "csv":
        return extract_text_from_csv(file)

    else:
        raise ValueError(f"Unsupported file type: {file_type}")
