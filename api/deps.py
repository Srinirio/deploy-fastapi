from pydantic import ValidationError
from db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from core import settings
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from core.config import settings
from schemas import *
from models import *
from crud import *
from core import *
import jwt
from schemas import TokenPayload


#oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
def authenticate(db: Session, email: str, password: str):
    user = getUserByEmail(db=db,email=email)
    if not user:
            return None
    if not verify_password(password, user.password):
            return None
    return user

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = getEmpById(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ):
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
):
    if not current_user.destination_id == 1:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_service_head(
    current_user: User = Depends(get_current_user),
):
    if not current_user.destination_id in [1,2]:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
        




