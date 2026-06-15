from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.orders import Order
from app.models.transaction import Transaction
from app.schemas.user import UserResponse
from app.schemas.orders import OrderResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

# VIEW ALL USERS
@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return db.query(User).all()

# VIEW ALL ORDERS
@router.get("/orders", response_model=list[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return db.query(Order).all()

# VIEW ALL TRANSACTIONS
@router.get("/transactions")
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return db.query(Transaction).all()