from sqlalchemy import Integer,String,Float,ForeignKey,Column
from app.database import Base

class Portfolio(Base):
    __tablename__="portfolio"
    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    stock_symbol=Column(String)
    quantity=Column(Integer)
    avg_price=Column(Float)
    