from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orders import Order
from app.models.stock import Stock
from app.models.portfoliotable import Portfolio
from app.models.transaction import Transaction
from app.schemas.orders import OrderCreate, OrderResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # check stock exists
    stock = db.query(Stock).filter(
        Stock.symbol == order.stock_symbol
    ).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # if SELL check enough shares
    if order.order_type == "SELL":
        portfolio = db.query(Portfolio).filter(
            Portfolio.user_id == current_user.id,
            Portfolio.stock_symbol == order.stock_symbol
        ).first()
        if not portfolio or portfolio.quantity < order.quantity:
            raise HTTPException(status_code=400, detail="Not enough shares")

    # create order
    new_order = Order(
        user_id=current_user.id,
        stock_symbol=order.stock_symbol,
        order_type=order.order_type,
        quantity=order.quantity,
        price=order.price,
        status="EXECUTED"
    )
    db.add(new_order)

    # update portfolio
    portfolio = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.stock_symbol == order.stock_symbol
    ).first()

    if order.order_type == "BUY":
        if portfolio:
            portfolio.quantity += order.quantity
        else:
            new_portfolio = Portfolio(
                user_id=current_user.id,
                stock_symbol=order.stock_symbol,
                quantity=order.quantity,
                avg_price=order.price
            )
            db.add(new_portfolio)

    elif order.order_type == "SELL":
        portfolio.quantity -= order.quantity
        if portfolio.quantity == 0:
            db.delete(portfolio)

    # create transaction log
    transaction = Transaction(
        user_id=current_user.id,
        stock_symbol=order.stock_symbol,
        transaction_type=order.order_type,
        quantity=order.quantity,
        price=order.price
    )
    db.add(transaction)

    db.commit()
    db.refresh(new_order)
    return new_order

# GET MY ORDERS
@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()