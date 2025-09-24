from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskOut   
from app.crud.task import create_task
from app.models.user import User
from app.authentication.dependencies import get_current_user
from app.crud.task import get_tasks_by_user, update_task, delete_task_by_user
from typing import List
from app.schemas.task import TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut)
def create_new_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_task(db, task, user_id=current_user.id)

@router.get("/get/tasks", response_model=List[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks_by_user(db, current_user.id)


@router.put("/update/{task_id}")
def update_tasks(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskOut:
    updated_task = update_task(db, task_id, task_data, current_user.id)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    
    return delete_task_by_user(db, task_id, current_user.id)