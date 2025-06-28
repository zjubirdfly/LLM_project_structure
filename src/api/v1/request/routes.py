from fastapi import APIRouter
from .vapi.outbound import router as outbound_router

router = APIRouter()

# Include the outbound router
router.include_router(outbound_router) 