from fastapi import APIRouter

from .v1.listings import router as listings_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(listings_router)
