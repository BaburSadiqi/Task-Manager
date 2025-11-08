from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.crud.task import create_task
from app.schemas.task import TaskCreate



def create_project(db: Session, project: ProjectCreate, owner_id: int):
    new_project = Project(
        name = project.name,
        description = project.description
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    default_tasks = [
        {"title": "Setup Repository", "description": "Initialize Git and basic structure"},
        {"title": "Requirement Analysis", "description": "Collect and Analyze requirement"},
        {"title": "Planning", "description": "Define sprint milestones and roadmap"}
    ]


    for task in default_tasks:
        task_data = TaskCreate(
            title=task["title"],
            description=task["description"],
            project_id=new_project.id
        )

        
        create_task(db, task_data, user_id=owner_id)

    db.commit()
    db.refresh(new_project)
    return new_project



def get_all_projects(db: Session):
    project = db.query(Project).all()
    return project
    

def get_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

def update_project(db: Session, project_id: int, project_data: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None
    
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return None
    
    db.delete(project)
    db.commit()
    return True
