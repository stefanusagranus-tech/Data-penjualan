import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Coba muat file .env (hanya dibaca saat dijalankan lokal)
load_dotenv()

# Mengambil variabel dari environment sistem atau file .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Variabel Supabase URL dan Key belum disetel di environment!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    return supabase
    
