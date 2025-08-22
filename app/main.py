from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base
from app.api.v1.api import api_router
from app.config import settings
from app.exceptions import MockCloudException
import logging

# Note: Database tables should be created using Alembic migrations
# Run: alembic upgrade head
# Or use the init script: python scripts/init_db.py

app = FastAPI(
    title="Mock Cloud API",
    description="""
    ## Mock Cloud API
    
    A comprehensive mock cloud backend API for testing, development, and SDK generation.
    
    ### Features
    * **Virtual Machines** - Create, manage, and monitor VMs
    * **Volumes** - Block storage management with VM attachment
    * **Security Groups** - Network security and access control
    * **Environments** - Network isolation with CIDR management
    * **Async Operations** - Background task processing with Celery
    
    ### Use Cases
    * **Development & Testing** - Mock cloud infrastructure
    * **SDK Development** - Generate client libraries
    * **Terraform Providers** - Infrastructure as code testing
    * **CI/CD Pipelines** - Automated testing environments
    
    ### Authentication
    No authentication required - suitable for development and testing.
    
    ### Rate Limiting
    No rate limiting applied - suitable for load testing.
    
    ### SDK Generation
    This API is designed to work seamlessly with OpenAPI code generators:
    * Python SDK generation
    * Go SDK generation  
    * Node.js SDK generation
    * Terraform provider development
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    servers=[
        {"url": "http://localhost:8000", "description": "Local Development"},
        {"url": "https://api.mockcloud.local", "description": "Production (example)"}
    ],
    contact={
        "name": "Mock Cloud API Support",
        "email": "support@mockcloud.local"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    tags_metadata=[
        {
            "name": "environments",
            "description": "Network environments with CIDR management. Each environment provides network isolation for resources.",
            "externalDocs": {
                "description": "Environment Management Guide",
                "url": "https://docs.mockcloud.local/environments"
            }
        },
        {
            "name": "vms",
            "description": "Virtual machine management. Create, monitor, and manage VMs with async provisioning.",
            "externalDocs": {
                "description": "VM Management Guide", 
                "url": "https://docs.mockcloud.local/vms"
            }
        },
        {
            "name": "volumes",
            "description": "Block storage volumes that can be attached to VMs. Supports creation, attachment, and lifecycle management.",
            "externalDocs": {
                "description": "Volume Management Guide",
                "url": "https://docs.mockcloud.local/volumes"
            }
        },
        {
            "name": "security-groups",
            "description": "Network security groups for controlling access to resources. Define ingress and egress rules.",
            "externalDocs": {
                "description": "Security Group Guide",
                "url": "https://docs.mockcloud.local/security-groups"
            }
        },
        {
            "name": "tasks",
            "description": "Background task management and monitoring. Track async operations like VM and volume provisioning.",
            "externalDocs": {
                "description": "Task Management Guide",
                "url": "https://docs.mockcloud.local/tasks"
            }
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Global exception handler
@app.exception_handler(MockCloudException)
async def mock_cloud_exception_handler(request: Request, exc: MockCloudException):
    """Handle MockCloudException globally"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code or "UNKNOWN_ERROR",
                "message": exc.detail,
                "status_code": exc.status_code,
                "resource_type": exc.resource_type,
                "resource_id": exc.resource_id
            }
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions globally"""
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "status_code": 500
            }
        }
    )

@app.get("/")
def root():
    return {
        "message": "Mock Cloud API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
