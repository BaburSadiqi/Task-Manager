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
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["auth"])




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
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}