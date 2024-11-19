
import datetime
from typing import Optional, Union
from pydantic import BaseModel



class User(BaseModel):
    id: int
    email: str
    created_at: datetime.datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None
    user: Optional[User] = None
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

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
    
   