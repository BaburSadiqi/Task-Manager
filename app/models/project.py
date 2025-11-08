from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Identity, ForeignKey, Text 
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import DateTime, func
from app.models.user import User

class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, Identity(), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    owner_id = Column(BigInteger, ForeignKey("public.users.id"))
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

