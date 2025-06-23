from fastapi import FastAPI
from database import engine
from models import Base
from routes import student_routes, class_routes

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(student_routes.router)
app.include_router(class_routes.router)

