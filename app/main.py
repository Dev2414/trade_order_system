from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.models.user import User
from app.models.transaction import Transaction
from app.models.stock import Stock
from app.models.portfoliotable import Portfolio
from app.models.orders import Order
from app.routers import auth, user, stocks, orders, admin, ai


ap = FastAPI()

# CREATE ALL TABLES
Base.metadata.create_all(bind=engine)

# INCLUDE ALL ROUTERS
ap.include_router(auth.router)
ap.include_router(user.router)
ap.include_router(stocks.router)
ap.include_router(orders.router)
ap.include_router(admin.router)
ap.include_router(ai.router) 

# HOME ROUTE
@ap.get("/")
def home():
    return {"message": "Trade Order System Running"}

# GLOBAL ERROR HANDLER
@ap.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


