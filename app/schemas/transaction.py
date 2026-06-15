from pydantic import BaseModel
from datetime import datetime

class TransactionResponse(BaseModel):
    id:int
    user_id:int
    stock_symbol:str
    transaction_type :str
    quantity :int
    price : float
    created_at:datetime

    class Config:
        from_attributes=True

        