from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None

    class Config:
        orm_mode = True


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: Optional[int] 
    created_at: datetime
    updated_at: Optional[datetime] 

    class Config:
        orm_mode = True


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
