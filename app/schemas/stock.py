from pydantic import BaseModel

class StockCreate(BaseModel):
    symbol: str
    name: str
    price: float

class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    price: float

    class Config:
        from_attributes = True