from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.models.task import Task
from app.models.project import Project
from app.routers import task
from app.authentication import routes as auth_routes
from app.routers import project 




Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_routes.router)
app.include_router(task.router) 
app.include_router(project.router)