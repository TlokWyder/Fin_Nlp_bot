from fastapi import APIRouter, HTTPException
from BackEnd.core.db import supabase
from schemas import CartItemIn

router = APIRouter()

@router.post("/add")
async def add_to_cart(item: CartItemIn):
        # FIX #1: cart_id теперь в теле запроса (item.cart_id), не query param
    try:
        prod = supabase.table("Products").select("stock_quantity")\
               .eq("id", item.product_id).single().execute()
    except Exception:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if prod.data["stock_quantity"] < item.quantity:
        raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

    result = supabase.table("CartItems").insert({
        "cart_id": item.cart_id,   # FIX #1: берём из тела
        "product_id": item.product_id,
        "quantity": item.quantity
    }).execute()
    return result.data

@router.get("/{cart_id}")
async def get_cart(cart_id: str):
    result = supabase.table("CartItems")\
             .select("*, Products(name, price)")\
             .eq("cart_id", cart_id).execute()
    return result.data