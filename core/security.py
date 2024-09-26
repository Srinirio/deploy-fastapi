import jwt
from datetime import datetime,timedelta,timezone
from core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user_id: str):
    data = {
        "sub":user_id,
        "exp":datetime.now()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    
    jwt_token = jwt.encode(data,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return jwt_token

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)