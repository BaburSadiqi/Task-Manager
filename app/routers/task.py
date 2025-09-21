from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskOut   
from app.crud.task import create_task
from app.models.user import User
from app.authentication.dependencies import get_current_user

router = APIRouter(prefix="/route", tags=["auth"])

@router.post("/task", response_model=TaskOut)
def create_new_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_task(db, task, user_id=current_user.id)