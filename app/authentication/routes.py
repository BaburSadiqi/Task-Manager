from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.authentication.utils import hashed_password
from passlib.context import CryptContext
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.models.user import User
from app.authentication.jwt_handler import create_access_token
from app.authentication.utils import verify_password
from app.authentication.schemas import Token, TokenDate

router = APIRouter(prefix="/auth", tags=["Authentication"])




@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password_value = hashed_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password_value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def user_login(user: UserLogin, db: Session = Depends(get_db)) -> Token:

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid password or username")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    

    token = create_access_token({"sub": db_user.username})
    return {"token": token, "token_type": "bearer"}