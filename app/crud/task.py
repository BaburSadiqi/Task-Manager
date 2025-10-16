from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException, status
from datetime import datetime
from app.utils.workflow import is_valid_transition



def create_task(db: Session, task: TaskCreate, user_id: int):
    new_task = Task(
        title = task.title,
        description = task.description,
        status = task.status,
        priority = task.priority,
        due_date = task.due_date,
        owner_id = user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



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
    return {"detail": "Task deleted seccessfully"}