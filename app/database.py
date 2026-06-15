from sqlalchemy import create_engine
#IT IS USED TO CREATE TO CREATE A CONNECTION WITH DATBASE URL HELP CREATE ACTUAL CONNECTION WITH POSTGREE DATABASE
from sqlalchemy.orm import sessionmaker,declarative_base
#IT IS USED TO CREATE SESSION IN DATABASE AND DECLARATIVE BASE IS USED TO GIVE MODELS INHERIT PROPERTION FROM ONE DATBASE
import os
#IT IS USED TO ACCESS DATA FROM ENV
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)

Sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
#bind is used to links the session to database engine
Base=declarative_base()

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
