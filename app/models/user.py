from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Identity
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, Identity(), primary_key=True, index=True)
    user_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


