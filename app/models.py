from datetime import datetime
from typing import Optional
from sqlalchemy import TIME, TIMESTAMP,Column,DateTime, ForeignKey
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    password: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,  # Automatically set to current timestamp
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    
        

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True
    rating: int = None
    created_at: datetime = Field(
        default_factory=datetime.utcnow,  # Automatically set to current timestamp
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    user_id: int = Field(sa_column=Column( ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    
    

