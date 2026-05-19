from fastapi import APIRouter, HTTPException, Depends
from BackEnd.core.db import supabase
from BackEnd.routers.schemas import CheckoutIn
from BackEnd.core.auth import get_current_user

router = APIRouter()

@router.post("/checkout")
async def checkout(data: CheckoutIn, current_user=Depends(get_current_user)):
    try:
        supabase.table("carts") \
            .select("id") \
            .eq("id", data.cart_id) \
            .eq("user_id", current_user.id) \
            .single() \
            .execute()
    except Exception:
        raise HTTPException(
            status_code=403,
            detail="Корзина не найдена или не принадлежит вам"
        )

    try:
        result = supabase.rpc("place_order", {
            "p_user_id": current_user.id,
            "p_cart_id": data.cart_id
        }).execute()
        return result.data
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


