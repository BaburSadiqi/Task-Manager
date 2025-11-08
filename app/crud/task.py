from fastapi import HTTPException, status 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException, status
from datetime import datetime
from app.utils.workflow import is_valid_transition
from app.models.user import User
from typing import Union, Any
from app.models.project import Project
from app.schemas.task import TaskCreate


def create_task(db: Session, task: Union[TaskCreate, dict, Any], user_id: int) -> Task:
    """
    Create and persist a Task. Accepts TaskCreate or dict-like payload.
    Validates foreign keys and handles integrity errors gracefully.
    """

    #  Normalize 
    if not isinstance(task, TaskCreate):
        try:
            task = TaskCreate.model_validate(task)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid task payload: {exc}"
            )

    # Validate Project existence
    if task.project_id is not None:
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {task.project_id} not found."
            )

    #  Create Task instance 
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        owner_id=user_id,
        project_id=task.project_id,
        assigned_to=task.assigned_to
    )

    
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e.orig)}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while creating task: {str(e)}"
        )


def get_tasks_by_user(db: Session, user_id: int, status: str = None, priority: str = None, due_date: datetime = None):
    query = db.query(Task).filter(Task.owner_id == user_id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if due_date:
        query = query.filter(Task.due_date == due_date)

    return query.all()


def update_task(
        db: Session,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int
) -> Task:
    """
    update a task by task_id and user_id with provided task_data.
    only status transitions are validated against workflow rules
    """



    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    if task_data.status is not None and task_data.status != task.status:
        if not is_valid_transition(task.status, task_data.status):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from {task.status} to {task_data.status}"
            )
        task.status = task_data.status
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority

    db.commit()
    db.refresh(task)
    return task

def delete_task_by_user(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}


def assign_task_to_user(db: Session, task_id: int, user_id: int, owner_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    

    project_owner_id = getattr(getattr(task, "project", None), "owner_id", None)
    if task.owner_id != owner_id and owner_id != project_owner_id:
        raise HTTPException(status_code=403, detail="Not authorized")
   #if task.owner_id != owner_id and owner_id != task.project.owner_id:
      #  raise HTTPException(status_code=403, detail="Not authorized")
    
    task.assigned_to = user_id
    db.commit()
    db.refresh(task)
    return task