from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import VMCreate, VMResponse, VMListResponse, TaskResponse
from app.services import VMService
from app.exceptions import MockCloudException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/", response_model=TaskResponse)
def create_vm(
    vm: VMCreate,
    db: Session = Depends(get_db)
):
    """Create a new VM"""
    try:
        result = VMService.create_vm(db, vm)
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

@router.get("/{vm_id}", response_model=VMResponse)
def get_vm(
    vm_id: int,
    db: Session = Depends(get_db)
):
    """Get VM by ID"""
    vm = VMService.get_vm(db, vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@router.get("/", response_model=VMListResponse)
def get_all_vms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all VMs"""
    vms, total = VMService.get_all_vms(db, skip, limit)
    return VMListResponse(
        vms=vms,
        total=total
    )

@router.delete("/{vm_id}", response_model=TaskResponse)
def delete_vm(
    vm_id: int,
    db: Session = Depends(get_db)
):
    """Delete VM"""
    result = VMService.delete_vm(db, vm_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return TaskResponse(
        task_id=result["task_id"],
        status="started",
        message=result["message"]
    )
