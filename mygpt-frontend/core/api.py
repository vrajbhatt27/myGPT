import logging

import requests
from config.settings import BACKEND_URL

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Starting up — BACKEND_URL = {BACKEND_URL}")


def ask_claude(question: str) -> str:
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask", json={"question": question}, timeout=5
        )
        response.raise_for_status()
        result = response.json()
        return result["answer"]
    except Exception as e:
        return f"ERROR: {e}"
