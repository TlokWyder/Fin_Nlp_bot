from dotenv import load_dotenv
import os

load_dotenv()  # читает .env файл из корня проекта

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Не найдены SUPABASE_URL или SUPABASE_KEY в .env")