from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException, status


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



def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    
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