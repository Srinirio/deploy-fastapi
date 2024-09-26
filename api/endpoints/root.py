from fastapi import APIRouter
from schemas import *

router = APIRouter()

@router.get("/",response_model=Message)
async def root():
    return {"message":"Hello World"}