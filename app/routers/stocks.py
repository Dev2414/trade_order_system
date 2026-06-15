from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/stocks", tags=["Stocks"])

# ADD STOCK (admin only)
@router.post("/", response_model=StockResponse)
def add_stock(
    stock: StockCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    existing = db.query(Stock).filter(
        Stock.symbol == stock.symbol
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Stock already exists")

    new_stock = Stock(
        symbol=stock.symbol,
        name=stock.name,
        price=stock.price
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

# GET ALL STOCKS
@router.get("/", response_model=list[StockResponse])
def get_stocks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Stock).all()

# UPDATE STOCK (admin only)
@router.put("/{symbol}", response_model=StockResponse)
def update_stock(
    symbol: str,
    stock: StockCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    db_stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    db_stock.price = stock.price
    db.commit()
    db.refresh(db_stock)
    return db_stock

# DELETE STOCK (admin only)
@router.delete("/{symbol}")
def delete_stock(
    symbol: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    db_stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    db.delete(db_stock)
    db.commit()
    return {"message": "Stock deleted"}