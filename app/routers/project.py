from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ProjectResponse
from app.crud import project as crud_project
from typing import List
from app.authentication.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = crud_project.create_project(db, project, owner_id=current_user.id)

    return new_project


@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    crud_project.get_all_projects(db)
    return crud_project


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db)
) -> ProjectOut:
    
    project = crud_project.get_project(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project_by_id(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
) -> ProjectOut:
    
    project = crud_project.update_project(db, project_id, project_data)

    if not project:
        raise HTTPException(status_code=403, detail="Project not found or not updated")
    
    return project


@router.delete("/{project_id}", response_model=dict)
def delete_project_by_id(
    project_id: int,
    db: Session = Depends(get_db)
) -> dict:
    
    result = crud_project.delete_project(db, project_id)

    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    
    
    return {"detail": "Project deleted successfully"}
    
    
