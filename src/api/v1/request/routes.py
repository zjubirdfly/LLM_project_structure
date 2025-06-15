from fastapi import APIRouter
from .vapi.outbound import router as vapi_router

router = APIRouter()

# Include routers under the same request router
router.include_router(vapi_router)