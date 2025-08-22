from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import EnvironmentCreate, EnvironmentResponse, EnvironmentListResponse
from app.services import EnvironmentService
from app.exceptions import MockCloudException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=EnvironmentResponse, tags=["environments"])
def create_environment(
    environment: EnvironmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new network environment.
    
    Creates an isolated network environment with a specified CIDR block.
    All resources (VMs, volumes) created within this environment will be
    network-isolated from other environments.
    
    **Use Cases:**
    * Development environment isolation
    * Multi-tenant infrastructure
    * Network security testing
    
    **Example:**
    ```json
    {
      "name": "prod-web",
      "network_cidr": "10.100.0.0/16",
      "description": "Production web environment"
    }
    ```
    """
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

@router.get("/{environment_id}", response_model=EnvironmentResponse, tags=["environments"])
def get_environment(
    environment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific environment by ID.
    
    Retrieves detailed information about a network environment including
    its CIDR block, creation time, and associated resources.
    
    **Parameters:**
    * `environment_id`: Unique identifier for the environment
    
    **Returns:**
    Complete environment information with metadata
    """
    try:
        environment = EnvironmentService.get_environment(db, environment_id)
        return environment
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=EnvironmentListResponse, tags=["environments"])
def get_all_environments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all environments with pagination.
    
    Retrieves a paginated list of all network environments.
    Useful for listing available environments and implementing
    pagination in client applications.
    
    **Parameters:**
    * `skip`: Number of environments to skip (for pagination)
    * `limit`: Maximum number of environments to return
    
    **Returns:**
    Paginated list of environments with total count
    """
    environments, total = EnvironmentService.get_all_environments(db, skip, limit)
    return EnvironmentListResponse(
        environments=environments,
        total=total
    )

@router.delete("/{environment_id}", tags=["environments"])
def delete_environment(
    environment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an environment by ID.
    
    Removes a network environment and all its associated resources.
    This operation is irreversible and will affect all VMs and volumes
    within the environment.
    
    **Parameters:**
    * `environment_id`: Unique identifier for the environment to delete
    
    **Returns:**
    Success message confirming deletion
    
    **Note:**
    This operation will fail if there are active resources in the environment.
    """
    try:
        success = EnvironmentService.delete_environment(db, environment_id)
        return {"message": "Environment deleted successfully"}
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
