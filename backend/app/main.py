"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core import settings, AppBaseError
from app.interfaces.routes_auth import router as auth_router
from app.interfaces.routes_projects import router as projects_router
from app.interfaces.routes_workspaces import router as workspaces_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup and shutdown."""
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready SaaS API with ",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for custom exceptions
@app.exception_handler(AppBaseError)
async def app_exception_handler(request, exc: AppBaseError):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# API v1 routes
@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
    }


# Include routers
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(workspaces_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
