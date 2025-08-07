from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import (
    UserLogin,
    UserCreate, UserOut
)
from app.models.user import User
from app.database import get_db
from passlib.context import CryptContext


router = APIRouter(prefix="/auth", tags=["Authentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    exiting_user = db.query(User).filter(User.user_name == user.username).first()
    
    if not exiting_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    hashed_passsword = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_passsword
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user