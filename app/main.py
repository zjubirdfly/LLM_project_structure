"""
FastAPI application entry point.
"""

import logging
from typing import List, Tuple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.api.v1.outbound import router as outbound_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LLM Demo",
        description="LLM DemoService with VAPI Integration",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # Include routers
    app.include_router(outbound_router, prefix="/api/v1", tags=["Outbound"])
    
    return app

def list_routes(app: FastAPI) -> List[Tuple[str, str]]:
    """List all registered endpoints in the application."""
    return [(route.path, ",".join(route.methods)) for route in app.routes]

def main() -> None:
    """Main entry point for the application."""
    # Print registered endpoints
    logger.info("Registered endpoints:")
    for path, methods in list_routes(app):
        logger.info(f"Endpoint: {path}, Methods: {methods}")
    
    # Start the server
    logger.info(f"Starting server on port {settings.port}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )

# Create the FastAPI app instance
app = create_app()

if __name__ == "__main__":
    main() 