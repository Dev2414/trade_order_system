from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__="orders"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    order_type=Column(String)
    price=Column(Float)
    quantity=Column(Integer)
    stock_symbol=Column(String)
    status=Column(String,default="executed")
    created_at=Column(DateTime,default=datetime.utcnow)
