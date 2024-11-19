from typing import Annotated
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT token
#Secret key
SECRET_KEY = "48d11d39652af5f09650164155324b032f7bb5e6a34d4003d73d0932e118e32"
ALGORITHM = "HS256"
ISSUER = "example.com"


def create_jwt_token(data: dict,expires_in: int = 60):
    expire_at = datetime.utcnow() + timedelta(minutes=expires_in)
    to_encode = {
        **data,
        "exp": expire_at,
        "iat": datetime.utcnow(),  # Issued at time
        "iss": ISSUER             # Issuer claim
        }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        
        if id is None:
            raise  credentials_exception
        token_data = schemas.TokenData(id=id)
    except  jwt.PyJWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: Annotated[schemas.UserResponse, Depends(oauth2_scheme)],session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Could not validate credentials', 
        headers={"WWW-Authenticate": "Bearer"},
        )
    print(token)
    token = decode_jwt_token(token,credentials_exception)
    if token is None:
        raise credentials_exception
    user =  session.query(models.User).filter(models.User.id == token.id).first()
    
    return user

CurrentUser = Depends(get_current_user)