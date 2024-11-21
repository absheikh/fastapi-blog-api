
import datetime
from typing import Annotated, Optional, Union
from unittest.mock import Base
from pydantic import BaseModel, conint



class User(BaseModel):
    id: int
    email: str
    created_at: datetime.datetime

class PostBase(BaseModel):
    id:int
    title: str
    content: str
    published: bool = True
    rating: int = None
    user: Optional[User] = None
    votes: int = 0
    

class PostOut(BaseModel):
    post: PostBase
    votes: int
    
class PostCreate(PostBase):
    title: str
    content: str
    published: bool = True
    rating: int = None

class PostUpdate(PostBase):
    title: str
    content: str
    published: bool = True
    rating: int = None

class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Union[list, dict]] = None
   
class UserBase(BaseModel):
    email: str
    password: str

class RegisterUser(UserBase):
    pass
    confirm_password: str
    
    
class LoginUser(UserBase):
    pass
    
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[int] = None
    
class UserResponse(BaseModel):
    user: Optional[User] = None
    token: Token = None
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]