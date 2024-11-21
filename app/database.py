from typing import Annotated
from . import models
from fastapi import Depends
from sqlmodel import  Session, create_engine
from .config import settings


engine = create_engine(settings.database_url)

session = Session(autocommit=False, autoflush=False, bind=engine)


    
def  create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
