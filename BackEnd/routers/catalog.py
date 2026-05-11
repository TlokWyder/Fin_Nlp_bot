from fastapi import APIRouter, HTTPException
from BackEnd.core.db import supabase
from BackEnd.routers.schemas import ProductOut

router = APIRouter()

@router.get("/products", response_model=list[ProductOut])
async def get_products():
    result = supabase.table("products").select("*").execute()
    return result.data

@router.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: int):
    try:
        result = supabase.table("products").select("*")\
                 .eq("id", product_id).single().execute()
        return result.data
    except Exception:
        raise HTTPException(status_code=404, detail="Товар не найден")

