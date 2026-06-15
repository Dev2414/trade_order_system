from sqlalchemy import Column,Integer,String,ForeignKey,Float
from app.database import Base

class Stock(Base):
    __tablename__="stocks"
    id=Column(Integer,primary_key=True,index=True)
    symbol=Column(String,unique=True,index=True)
    name=Column(String)
    price=Column(Float)
