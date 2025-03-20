import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CACHE_NAME = os.getenv("DB_CACHE_NAME", "")
DB_CACHE_USER = os.getenv("DB_CACHE_USER", "")
DB_CACHE_PASSWORD = os.getenv("DB_CACHE_PASSWORD", "")
DB_CACHE_HOST = os.getenv("DB_CACHE_HOST", "")
DB_CACHE_PORT = os.getenv("DB_CACHE_PORT", "")
DB_CACHE_TABLE_NAME = os.getenv("DB_CACHE_TABLE_NAME", "")
DB_CACHE_URL = os.getenv("DB_CACHE_URL", "")
GOOGLE_MAPS_API = os.getenv("GOOGLE_MAPS_API", "")
