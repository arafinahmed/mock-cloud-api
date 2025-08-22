from pydantic import BaseModel, Field
from typing import Optional
from collections.abc import Sequence
from datetime import datetime
from app.models import VMStatus, VolumeStatus, ResourceStatus

# Base schemas
class EnvironmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    network_cidr: str = Field(default="10.0.0.0/16")
    description: Optional[str] = None

class SecurityGroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    rules: Optional[str] = None

class VMBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    instance_type: str = Field(..., min_length=1, max_length=50)
    environment_id: int
    security_group_id: Optional[int] = None

class VolumeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    size_gb: int = Field(..., gt=0, le=10000)
    environment_id: int
    vm_id: Optional[int] = None

# Create schemas
class EnvironmentCreate(EnvironmentBase):
    pass

class SecurityGroupCreate(SecurityGroupBase):
    pass

class VMCreate(VMBase):
    pass

class VolumeCreate(VolumeBase):
    pass

# Response schemas
class EnvironmentResponse(EnvironmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class SecurityGroupResponse(SecurityGroupBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class VMResponse(VMBase):
    id: int
    status: VMStatus
    resource_status: ResourceStatus
    ip_address: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class VolumeResponse(VolumeBase):
    id: int
    status: VolumeStatus
    resource_status: ResourceStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

# List response schemas
class EnvironmentListResponse(BaseModel):
    environments: Sequence[EnvironmentResponse]
    total: int

class SecurityGroupListResponse(BaseModel):
    security_groups: Sequence[SecurityGroupResponse]
    total: int

class VMListResponse(BaseModel):
    vms: Sequence[VMResponse]
    total: int

class VolumeListResponse(BaseModel):
    volumes: Sequence[VolumeResponse]
    total: int

# Task schemas
class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
    id: Optional[int] = None
    resource_type: Optional[str] = None

# Resource creation response schemas
class ResourceCreateResponse(BaseModel):
    id: int
    name: str
    status: str
    message: str
    task_id: str

# Error response schemas
class ErrorResponse(BaseModel):
    error: dict
