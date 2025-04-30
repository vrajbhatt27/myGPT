from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Set the default URL for the backend
default_url = "http://localhost:8000"

BACKEND_URL = os.getenv("BACKEND_URL", default_url)