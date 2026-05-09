from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY

# Синглтон — один клиент на всё приложение, не переподключаемся на каждый запрос
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)