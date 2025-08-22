from fastapi import APIRouter
from app.api.v1.endpoints import environments, security_groups, vms, volumes

api_router = APIRouter()

api_router.include_router(environments.router, prefix="/environments", tags=["environments"])
api_router.include_router(security_groups.router, prefix="/security-groups", tags=["security-groups"])
api_router.include_router(vms.router, prefix="/vms", tags=["vms"])
api_router.include_router(volumes.router, prefix="/volumes", tags=["volumes"])
