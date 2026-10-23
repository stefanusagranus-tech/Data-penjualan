import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_supabase_client
from supabase import Client

app = FastAPI(
    title="Data Penjualan API",
    description="Backend modern berbasis FastAPI dan Supabase.",
    version="1.0.0"
)

# Mengatur CORS agar nanti bisa diakses oleh frontend dengan lancar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "API Data Penjualan berjalan dengan baik! 🚀"}

@app.get("/api/sales")
def get_sales_data(supabase: Client = Depends(get_supabase_client)):
    try:
        # Mengambil data dari tabel Supabase (sesuaikan nama tabelnya, misal 'tx_tsale' atau lainnya)
        response = supabase.table("tx_tsale").select("*").limit(50).execute()
        return {
            "status": "success",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/all-tables")
def get_all_tables(supabase: Client = Depends(get_supabase_client)):
    try:
        # Mengambil data dari seluruh tabel utama
        sales_store = supabase.table("sales_store").select("*").execute().data
        sales_item = supabase.table("sales_item").select("*").execute().data
        sales_pps = supabase.table("sales_pps").select("*").execute().data
        master_item = supabase.table("master_item").select("*").execute().data
        master_personil = supabase.table("master_personil").select("*").execute().data
        
        return {
            "status": "success",
            "data": {
                "sales_store": sales_store,
                "sales_item": sales_item,
                "sales_pps": sales_pps,
                "master_item": master_item,
                "master_personil": master_personil
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
