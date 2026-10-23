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
