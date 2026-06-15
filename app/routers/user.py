from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.orders import Order
from app.models.portfoliotable import Portfolio
from app.database import get_db
from app.schemas.orders import OrderCreate,OrderResponse
from app.schemas.portfoliotable import PortfolioResponse

router = APIRouter(prefix="/user", tags=["User"])

#get my profile
@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

#get my orders
@router.get("/orders",response_model=list[OrderResponse])
def orders(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

#get my portfolio
@router.get("/portfolio",response_model=list[PortfolioResponse])
def portfolio(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    return portfolio
    