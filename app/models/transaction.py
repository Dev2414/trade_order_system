from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__="Transaction"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    stock_symbol=Column(String)
    transaction_type = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    created_at=Column(DateTime,default=datetime.utcnow())
    