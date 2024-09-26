from fastapi import APIRouter,Depends,HTTPException, status
from api.deps import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from core import security
from crud import *
from schemas import Token
from api.deps import *

router = APIRouter()

"""
This is for login form - Here we do authentication
"""    
@router.post("/login/access-token",response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }