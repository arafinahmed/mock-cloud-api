from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import VolumeCreate, VolumeResponse, VolumeListResponse, TaskResponse
from app.services import VolumeService

router = APIRouter()

@router.post("/", response_model=TaskResponse)
def create_volume(
    volume: VolumeCreate,
    db: Session = Depends(get_db)
):
    """Create a new volume"""
    try:
        result = VolumeService.create_volume(db, volume)
        return TaskResponse(
            task_id=result["task_id"],
            status="started",
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{volume_id}", response_model=VolumeResponse)
def get_volume(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """Get volume by ID"""
    volume = VolumeService.get_volume(db, volume_id)
    if not volume:
        raise HTTPException(status_code=404, detail="Volume not found")
    return volume

@router.get("/", response_model=VolumeListResponse)
def get_all_volumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all volumes"""
    volumes = VolumeService.get_all_volumes(db, skip, limit)
    return VolumeListResponse(
        volumes=volumes,
        total=len(volumes)
    )

@router.delete("/{volume_id}", response_model=TaskResponse)
def delete_volume(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """Delete volume"""
    result = VolumeService.delete_volume(db, volume_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return TaskResponse(
        task_id=result["task_id"],
        status="started",
        message=result["message"]
    )

@router.post("/{volume_id}/attach/{vm_id}")
def attach_volume_to_vm(
    volume_id: int,
    vm_id: int,
    db: Session = Depends(get_db)
):
    """Attach volume to VM"""
    success = VolumeService.attach_volume_to_vm(db, volume_id, vm_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to attach volume to VM")
    return {"message": "Volume attached to VM successfully"}

@router.post("/{volume_id}/detach")
def detach_volume_from_vm(
    volume_id: int,
    db: Session = Depends(get_db)
):
    """Detach volume from VM"""
    success = VolumeService.detach_volume_from_vm(db, volume_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to detach volume from VM")
    return {"message": "Volume detached from VM successfully"}
