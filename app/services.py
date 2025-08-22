from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models import VM, Volume, Environment, SecurityGroup
from app.schemas import VMCreate, VolumeCreate, EnvironmentCreate, SecurityGroupCreate
from app.worker import create_vm_task, create_volume_task, delete_vm_task, delete_volume_task
from app.database_utils import (
    create_resource, get_resource_by_id, list_resources, 
    delete_resource, check_resource_exists, safe_commit
)
from app.exceptions import (
    ResourceNotFoundException, ResourceAlreadyExistsException,
    ValidationException, ResourceOperationException
)

class EnvironmentService:
    @staticmethod
    def create_environment(db: Session, environment: EnvironmentCreate) -> Environment:
        # Check if environment with same name already exists
        if check_resource_exists(db, Environment, "name", environment.name, "environment"):
            raise ResourceAlreadyExistsException(
                resource_type="environment",
                resource_name=environment.name
            )
        
        return create_resource(db, Environment, environment.dict(), "environment")
    
    @staticmethod
    def get_environment(db: Session, environment_id: int) -> Environment:
        return get_resource_by_id(db, Environment, environment_id, "environment")
    
    @staticmethod
    def get_all_environments(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[Environment], int]:
        return list_resources(db, Environment, skip, limit)
    
    @staticmethod
    def delete_environment(db: Session, environment_id: int) -> bool:
        return delete_resource(db, Environment, environment_id, "environment")

class SecurityGroupService:
    @staticmethod
    def create_security_group(db: Session, security_group: SecurityGroupCreate) -> SecurityGroup:
        # Check if security group with same name already exists
        if check_resource_exists(db, SecurityGroup, "name", security_group.name, "security_group"):
            raise ResourceAlreadyExistsException(
                resource_type="security_group",
                resource_name=security_group.name
            )
        
        return create_resource(db, SecurityGroup, security_group.dict(), "security_group")
    
    @staticmethod
    def get_security_group(db: Session, security_group_id: int) -> SecurityGroup:
        return get_resource_by_id(db, SecurityGroup, security_group_id, "security_group")
    
    @staticmethod
    def get_all_security_groups(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[SecurityGroup], int]:
        return list_resources(db, SecurityGroup, skip, limit)
    
    @staticmethod
    def delete_security_group(db: Session, security_group_id: int) -> bool:
        return delete_resource(db, SecurityGroup, security_group_id, "security_group")

class VMService:
    @staticmethod
    def create_vm(db: Session, vm: VMCreate) -> dict:
        # Check if VM with same name already exists
        if check_resource_exists(db, VM, "name", vm.name, "vm"):
            raise ResourceAlreadyExistsException(
                resource_type="vm",
                resource_name=vm.name
            )
        
        # Create VM record in database
        db_vm = create_resource(db, VM, vm.dict(), "vm")
        
        # Start Celery task for VM creation
        task = create_vm_task.delay({"id": db_vm.id})
        
        return {
            "vm": db_vm,
            "task_id": task.id,
            "message": "VM creation started",
            "resource_id": db_vm.id,
            "resource_type": "vm"
        }
    
    @staticmethod
    def get_vm(db: Session, vm_id: int) -> VM:
        return get_resource_by_id(db, VM, vm_id, "vm")
    
    @staticmethod
    def get_all_vms(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[VM], int]:
        return list_resources(db, VM, skip, limit)
    
    @staticmethod
    def delete_vm(db: Session, vm_id: int) -> dict:
        # Verify VM exists before starting deletion
        vm = get_resource_by_id(db, VM, vm_id, "vm")
        
        # Start Celery task for VM deletion
        task = delete_vm_task.delay(vm_id)
        
        return {
            "success": True,
            "task_id": task.id,
            "message": "VM deletion started",
            "resource_id": vm_id,
            "resource_type": "vm"
        }

class VolumeService:
    @staticmethod
    def create_volume(db: Session, volume: VolumeCreate) -> dict:
        # Check if volume with same name already exists
        if check_resource_exists(db, Volume, "name", volume.name, "volume"):
            raise ResourceAlreadyExistsException(
                resource_type="volume",
                resource_name=volume.name
            )
        
        # Create volume record in database
        db_volume = create_resource(db, Volume, volume.dict(), "volume")
        
        # Start Celery task for volume creation
        task = create_volume_task.delay({"id": db_volume.id})
        
        return {
            "volume": db_volume,
            "task_id": task.id,
            "message": "Volume creation started",
            "resource_id": db_volume.id,
            "resource_type": "volume"
        }
    
    @staticmethod
    def get_volume(db: Session, volume_id: int) -> Volume:
        return get_resource_by_id(db, Volume, volume_id, "volume")
    
    @staticmethod
    def get_all_volumes(db: Session, skip: int = 0, limit: int = 100) -> tuple[List[Volume], int]:
        return list_resources(db, Volume, skip, limit)
    
    @staticmethod
    def delete_volume(db: Session, volume_id: int) -> dict:
        # Verify volume exists before starting deletion
        volume = get_resource_by_id(db, Volume, volume_id, "volume")
        
        # Start Celery task for volume deletion
        task = delete_volume_task.delay(volume_id)
        
        return {
            "success": True,
            "task_id": task.id,
            "message": "Volume deletion started",
            "resource_id": volume_id,
            "resource_type": "volume"
        }
    
    @staticmethod
    def attach_volume_to_vm(db: Session, volume_id: int, vm_id: int) -> bool:
        volume = get_resource_by_id(db, Volume, volume_id, "volume")
        vm = get_resource_by_id(db, VM, vm_id, "vm")
        
        volume.vm_id = vm_id
        volume.status = VolumeStatus.IN_USE
        safe_commit(db, f"attach volume {volume_id} to VM {vm_id}")
        return True
    
    @staticmethod
    def detach_volume_from_vm(db: Session, volume_id: int) -> bool:
        volume = get_resource_by_id(db, Volume, volume_id, "volume")
        
        volume.vm_id = None
        volume.status = VolumeStatus.AVAILABLE
        safe_commit(db, f"detach volume {volume_id} from VM")
        return True
