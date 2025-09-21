from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum


class PlaceStatus(str, enum.Enum):
    """Enum for place status"""

    
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    completed = "COMPLETED"
    cancelled = "CANCELLED"

class Priority(str, enum.Enum):
    """Enum for place priority"""
    

    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"


class TaskCreate(BaseModel):
    status: Optional[PlaceStatus] = PlaceStatus.pending
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    priority: Optional[Priority] = Priority.medium
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    status: Optional[PlaceStatus] = None



class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority
    due_date: Optional[datetime] = None
    status: PlaceStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        orm_mode = True

