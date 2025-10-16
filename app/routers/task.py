from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskOut   
from app.crud.task import create_task
from app.models.user import User
from app.authentication.dependencies import get_current_user
from app.crud.task import get_tasks_by_user, update_task, delete_task_by_user
from typing import List, Optional, Any
from app.schemas.task import TaskUpdate
from fastapi import Query
from datetime import datetime

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
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    due_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks_by_user(
        db, current_user.id,
        status=status,
        priority=priority,
        due_date=due_date
    )


@router.put("/update/{task_id}", response_model=TaskOut)
def update_tasks(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a task. Only the owner can update the task.
    Status transitions are validated against workflow rules.
    """
    task = update_task(db, task_id, task_data, current_user.id)
    return task


@router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    
    return delete_task_by_user(db, task_id, current_user.id)