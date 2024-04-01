from fastapi import APIRouter

from server.api.routes import claims

api_router = APIRouter()
api_router.include_router(claims.router, prefix="/users", tags=["users"])
