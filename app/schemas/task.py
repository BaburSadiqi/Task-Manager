from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum


class PlaceStatus(str, enum.Enum):
    """Enum for place status"""

    
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    review = "REVIEW"
    testing = "TESTING"
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
    assigned_to: Optional[int] = None
    project_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    status: Optional[PlaceStatus] = None
    assigned_to: Optional[int] = None



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
    assigned_to: Optional[int] = None
    project_id: Optional[int] = None

    class Config:
        orm_mode = True

class AssignTaskUser(BaseModel):
    assigned_to: int