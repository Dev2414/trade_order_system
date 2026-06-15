from pydantic import BaseModel

class PortfolioResponse(BaseModel):
    id : int
    user_id:int
    stock_symbol:str
    quantity:int
    avg_price:float

    class Config:
        from_attributes=True
