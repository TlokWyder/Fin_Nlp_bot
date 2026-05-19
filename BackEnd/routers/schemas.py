from pydantic import BaseModel

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int

class CartItemIn(BaseModel):
    cart_id: str
    product_id: int
    quantity: int = 1

class MessageIn(BaseModel):
    chat_id: str
    text: str

class CheckoutIn(BaseModel):
    cart_id: str