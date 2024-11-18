
from fastapi import Depends, FastAPI, Response,status,HTTPException,Query, APIRouter
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

@router.post("/login", response_model=schemas.UserResponse)
def login_user(user_data:schemas.LoginUser,session:SessionDep):
    user = session.exec(select(models.User).where(models.User.email == user_data.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")
    if not utils.verify(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"success": True, "message": "User logged in successfully", "data": user.model_dump()}
    

  