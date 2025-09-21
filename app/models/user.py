from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Identity
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, Identity(), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)


    tasks = relationship("Task", back_populates="owner")


