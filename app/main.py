"""
Author:Cristian Martin Bessone
Email: cristian.bessone@gmail.com
Project: Code Challenge Qventus
Created: 25-APRIL-2025
Description: FastAPI service to allow CRUD operations for managing parts via RESTful API.
"""

from fastapi import FastAPI
from app.routers import part_router
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Parts API", version="1.0")


@app.get("/")
def say_hello():
    return "Server is running"


app.include_router(part_router.router)
