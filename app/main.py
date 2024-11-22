from sys import prefix
from typing import Annotated
from fastapi import Depends, FastAPI
from .database import  create_db_and_tables
from .routers import auth, posts, votes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="FastAPI SQLModel", version="0.1.0")


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
        
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/status")
async def root():
    return {"message": "Deployed using CI/CD pipeline with Github Actions"} 



  