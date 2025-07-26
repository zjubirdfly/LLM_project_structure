"""
FastAPI application entry point.
"""

from typing import List, Tuple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core import settings
from app.api.v1.outbound import router as outbound_router
from app.api.v1.custom_llm_request_handler import (
    router as custom_llm_request_handler_router,
)
from app.log_utils import Logger


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LLM Demo",
        description="LLM DemoService with VAPI Integration",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    # Include routers
    app.include_router(outbound_router, prefix="/api/v1", tags=["Outbound"])
    app.include_router(
        custom_llm_request_handler_router, tags=["Custom LLM Request Handler"]
    )
    Logger.log_system("Created FastAPI application with CORS enabled")
    return app


def list_routes(app: FastAPI) -> List[Tuple[str, str]]:
    """List all registered endpoints in the application."""
    return [(route.path, ",".join(route.methods)) for route in app.routes]


def main() -> None:
    """Main entry point for the application."""
    # Print registered endpoints
    Logger.log_system("Registered endpoints:")
    for path, methods in list_routes(app):
        Logger.log_system(f"Endpoint: {path}, Methods: {methods}")

    # Start the server
    Logger.log_system(f"Starting server on port {settings.port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=True)


# Create the FastAPI app instance
app = create_app()

if __name__ == "__main__":
    main()
