from fastapi import FastAPI
from app.database import Base, engine
from app.authentication import routes as auth_routes  

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_routes.router)