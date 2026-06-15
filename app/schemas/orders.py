from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    order_type:str
    price:float
    quantity:int
    stock_symbol:str

class OrderResponse(BaseModel):
    id:int
    user_id:int
    order_type:str
    price:float
    quantity:int
    stock_symbol:str
    status:str
    created_at:datetime

    class Config:
        from_attributes=True
