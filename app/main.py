"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

from app.config import settings
from app.db import get_pool, close_pool
from app.api.v1.outscraper.business import router as business_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/var/log/outscraper-api.log"),
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
# Set root_path for reverse proxy deployment
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="High-performance API for querying Outscraper business database",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/api/v1/outscraper",  # Required for reverse proxy to generate correct URLs
)

# Use OpenAPI 3.0.2 for better compatibility with Swagger UI and ReDoc
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="High-performance API for querying Outscraper business database",
        routes=app.routes,
        openapi_version="3.0.2",  # Use 3.0.2 instead of 3.1.0 for better compatibility
    )
    # Add servers field for proper Swagger UI rendering behind reverse proxy
    # Use relative URL since we're behind nginx reverse proxy
    openapi_schema["servers"] = [
        {
            "url": "https://data.eagleinfoservice.com/api/v1/outscraper",
            "description": "Production server"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Note: No prefix needed here since nginx strips /api/v1/outscraper/ before proxying
app.include_router(business_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database pool on startup"""
    logger.info("Starting Outscraper API...")
    try:
        await get_pool()
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database pool: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database pool on shutdown"""
    logger.info("Shutting down Outscraper API...")
    await close_pool()
    logger.info("Database connection pool closed")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        pool = await get_pool()
        # Test database connection
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "database": "connected",
                "pool_size": {
                    "min": settings.DB_POOL_MIN_SIZE,
                    "max": settings.DB_POOL_MAX_SIZE,
                }
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }
