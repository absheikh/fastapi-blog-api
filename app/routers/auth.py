
from typing import Annotated
from fastapi import Depends, FastAPI, Response,status,HTTPException,Query, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,utils
from sqlmodel import select
from ..database import SessionDep

router = APIRouter(tags=["Auth"], prefix="/api/v1/auth")


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data:schemas.RegisterUser,session:SessionDep):

    # check if password and confirm password match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # remove confirm_password from user_data
    user_data = user_data.model_dump(exclude={"confirm_password"})
    # Check if user already exists
    user = session.exec(select(models.User).where(models.User.email == user_data['email'])).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    # hash password
    hashed_password = utils.hash(user_data['password'])
    user_data["password"] = hashed_password
    user = models.User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    if  user:
        return {"success": True, "message": "User created successfully", "data": user.model_dump()}
    raise HTTPException(status_code=400, detail="User not created")

@router.post("/login", response_model=schemas.Token)
def login_user(user_data:Annotated[OAuth2PasswordRequestForm, Depends()], session:SessionDep):
    user = session.exec(select(models.User).where(models.User.email == user_data.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    if not utils.verify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
    # create jwt token
    token = utils.create_jwt_token({"user_id": user.id})
    #add token to response model
    return  schemas.Token(access_token=token, token_type="bearer")
    

  