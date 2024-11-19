from sys import prefix
from typing import Annotated
from fastapi import Depends, FastAPI
from .database import  create_db_and_tables
from .routers import auth, posts
from . import config


app = FastAPI(title="FastAPI SQLModel", version="0.1.0")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
        
app.include_router(auth.router)
app.include_router(posts.router)



  