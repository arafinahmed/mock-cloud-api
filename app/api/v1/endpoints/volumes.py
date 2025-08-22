from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import VolumeCreate, VolumeResponse, VolumeListResponse, TaskResponse
from app.services import VolumeService
from app.exceptions import MockCloudException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=TaskResponse, tags=["volumes"])
def create_volume(
    volume: VolumeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new volume.
    
    Creates a block storage volume that can be attached to VMs.
    Volume creation is asynchronous and takes 30-60 seconds.
    
    **Parameters:**
    * `name`: Unique name for the volume
    * `size_gb`: Size in gigabytes
    * `environment_id`: ID of the environment to create the volume in
    
    **Returns:**
    Task response with volume ID and task tracking information
    """
    try:
        result = VolumeService.create_volume(db, volume)
        return TaskResponse(
            task_id=result["task_id"],
            status="started",
            message=result["message"],
            id=result["id"],
            resource_type=result["resource_type"]
        )
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{volume_id}", response_model=VolumeResponse, tags=["volumes"])
def get_volume(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific volume by ID.
    
    Retrieves detailed information about a volume including
    its size, status, and attachment information.
    
    **Parameters:**
    * `volume_id`: Unique identifier for the volume
    
    **Returns:**
    Complete volume information with metadata
    """
    try:
        volume = VolumeService.get_volume(db, volume_id)
        return volume
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=VolumeListResponse, tags=["volumes"])
def get_all_volumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all volumes with pagination.
    
    Retrieves a paginated list of all volumes.
    Useful for listing available volumes and implementing
    pagination in client applications.
    
    **Parameters:**
    * `skip`: Number of volumes to skip (for pagination)
    * `limit`: Maximum number of volumes to return
    
    **Returns:**
    Paginated list of volumes with total count
    """
    try:
        volumes, total = VolumeService.get_all_volumes(db, skip, limit)
        return VolumeListResponse(
            volumes=volumes,
            total=total
        )
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{volume_id}", response_model=TaskResponse, tags=["volumes"])
def delete_volume(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a volume by ID.
    
    Starts the deletion process for a volume.
    Volume deletion is asynchronous and may take time
    if the volume is currently attached to a VM.
    
    **Parameters:**
    * `volume_id`: Unique identifier for the volume to delete
    
    **Returns:**
    Task response with deletion task information
    
    **Note:**
    This operation will fail if the volume is currently attached to a VM.
    """
    try:
        result = VolumeService.delete_volume(db, volume_id)
        return TaskResponse(
            task_id=result["task_id"],
            status="started",
            message=result["message"],
            resource_id=result["resource_id"],
            resource_type=result["resource_type"]
        )
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{volume_id}/attach/{vm_id}", tags=["volumes"])
def attach_volume_to_vm(
    volume_id: int,
    vm_id: int,
    db: Session = Depends(get_db)
):
    """
    Attach a volume to a VM.
    
    Attaches a volume to a specific VM, making it available
    for use by the VM. The volume status will change to 'in_use'.
    
    **Parameters:**
    * `volume_id`: Unique identifier for the volume
    * `vm_id`: Unique identifier for the VM to attach to
    
    **Returns:**
    Success message confirming attachment
    
    **Note:**
    A volume can only be attached to one VM at a time.
    """
    try:
        success = VolumeService.attach_volume_to_vm(db, volume_id, vm_id)
        return {"message": "Volume attached to VM successfully"}
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{volume_id}/detach", tags=["volumes"])
def detach_volume_from_vm(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """
    Detach a volume from its current VM.
    
    Detaches a volume from the VM it's currently attached to.
    The volume status will change to 'available' and can be
    attached to another VM.
    
    **Parameters:**
    * `volume_id`: Unique identifier for the volume to detach
    
    **Returns:**
    Success message confirming detachment
    """
    try:
        success = VolumeService.detach_volume_from_vm(db, volume_id)
        return {"message": "Volume detached from VM successfully"}
    except MockCloudException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
