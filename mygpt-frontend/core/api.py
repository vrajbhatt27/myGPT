# frontend/core/api.py

import logging

import requests
from config.settings import BACKEND_URL

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Starting up — BACKEND_URL = {BACKEND_URL}")


def ask_claude(question: str, uploaded_file=None) -> str:
    """
    Sends user question + uploaded file (if any) to backend /ask route.
    """
    try:
        files = {}

        if uploaded_file:
            # Streamlit's uploaded_file is a BytesIO-like object
            files["file"] = (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )

        data = {
            "question": question,
        }
        print("-----2----->", data)
        response = requests.post(
            f"{BACKEND_URL}/ask", data=data, files=files, timeout=10
        )

        response.raise_for_status()
        result = response.json()
        return result["answer"]

    except Exception as e:
        return f"ERROR: {e}"
