from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import EnvironmentCreate, EnvironmentResponse, EnvironmentListResponse
from app.services import EnvironmentService
from app.exceptions import MockCloudException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=EnvironmentResponse)
def create_environment(
    environment: EnvironmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new environment"""
    try:
        db_environment = EnvironmentService.create_environment(db, environment)
        return db_environment
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{environment_id}", response_model=EnvironmentResponse)
def get_environment(
    environment_id: int,
    db: Session = Depends(get_db)
):
    """Get environment by ID"""
    environment = EnvironmentService.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")
    return environment

@router.get("/", response_model=EnvironmentListResponse)
def get_all_environments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all environments"""
    environments, total = EnvironmentService.get_all_environments(db, skip, limit)
    return EnvironmentListResponse(
        environments=environments,
        total=total
    )

@router.delete("/{environment_id}")
def delete_environment(
    environment_id: int,
    db: Session = Depends(get_db)
):
    """Delete environment"""
    success = EnvironmentService.delete_environment(db, environment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Environment not found")
    return {"message": "Environment deleted successfully"}
