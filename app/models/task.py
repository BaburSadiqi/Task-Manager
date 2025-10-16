from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Identity, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship
from app.schemas.task import PlaceStatus, Priority
from sqlalchemy import Enum

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'schema': 'public'}


    id = Column(BigInteger, Identity(), primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(PlaceStatus, name="task_status"), default=PlaceStatus.pending, nullable=False)
    priority = Column(Enum(Priority, name="task_priority"), default=Priority.medium, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    owner_id = Column(BigInteger, ForeignKey("public.users.id"))
    owner = relationship("User", back_populates="tasks")
    project_id = Column(BigInteger, ForeignKey=("public.projects.id"))
    project = relationship("Projects", back_populates="tasts")

