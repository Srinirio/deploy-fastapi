from fastapi import APIRouter
from api.endpoints import *

api_router = APIRouter()

api_router.include_router(root.router, tags=["Root"])
api_router.include_router(login_api.router, tags=["Login"])
api_router.include_router(super_user_api.router, tags=["Super User"])
api_router.include_router(ticket_api.router, tags=["Ticket"])
api_router.include_router(service_head_api.router, tags=["Service Head"])
api_router.include_router(service_engineer_api.router, tags=["Service Engineer"])

