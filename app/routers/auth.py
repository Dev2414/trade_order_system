from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from app.database import get_db
from app.schemas.user import UserCreate,UserResponse,Userlogin
from app.utils.security import verify_password,hash_password
from app.utils.jwt import create_token
from app.models.user import User

router=APIRouter()
@router.post("/signup",response_model=UserResponse)

def signup(user:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()    
    if existing:
        raise HTTPException(status_code=400,detail='email already exist')
    
    new_user=User(
        username=user.username,
        password=hash_password(user.password),
        email=user.email 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user:Userlogin,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="user not present")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    token = create_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

