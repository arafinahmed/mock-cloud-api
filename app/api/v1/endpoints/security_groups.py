from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import SecurityGroupCreate, SecurityGroupResponse, SecurityGroupListResponse
from app.services import SecurityGroupService

router = APIRouter()

@router.post("/", response_model=SecurityGroupResponse)
def create_security_group(
    security_group: SecurityGroupCreate,
    db: Session = Depends(get_db)
):
    """Create a new security group"""
    try:
        db_security_group = SecurityGroupService.create_security_group(db, security_group)
        return db_security_group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{security_group_id}", response_model=SecurityGroupResponse)
def get_security_group(
    security_group_id: int,
    db: Session = Depends(get_db)
):
    """Get security group by ID"""
    security_group = SecurityGroupService.get_security_group(db, security_group_id)
    if not security_group:
        raise HTTPException(status_code=404, detail="Security group not found")
    return security_group

@router.get("/", response_model=SecurityGroupListResponse)
def get_all_security_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all security groups"""
    security_groups = SecurityGroupService.get_all_security_groups(db, skip, limit)
    return SecurityGroupListResponse(
        security_groups=security_groups,
        total=len(security_groups)
    )

@router.delete("/{security_group_id}")
def delete_security_group(
    security_group_id: int,
    db: Session = Depends(get_db)
):
    """Delete security group"""
    success = SecurityGroupService.delete_security_group(db, security_group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Security group not found")
    return {"message": "Security group deleted successfully"}
