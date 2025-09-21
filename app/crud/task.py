from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate



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