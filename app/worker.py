import random
import time
from celery import Celery
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import VM, Volume, Environment, SecurityGroup, VMStatus, VolumeStatus, ResourceStatus
from app.config import settings

# Create Celery app
celery_app = Celery(
    "mock_cloud_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.worker"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

def get_db_session():
    """Get database session for worker tasks"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

@celery_app.task(bind=True)
def create_vm_task(self, vm_data: dict):
    """Create VM task with random failure and timing"""
    db = get_db_session()
    
    try:
        # Check if VM exists
        vm = db.query(VM).filter(VM.id == vm_data["id"]).first()
        if not vm:
            return {"status": "failed", "message": "VM not found"}
        
        # Update status to creating
        vm.resource_status = ResourceStatus.CREATING
        vm.status = VMStatus.STARTING
        db.commit()
        
        # Simulate random failure (1/10 chance)
        if random.random() < settings.worker_failure_rate:
            vm.resource_status = ResourceStatus.FAILED
            vm.status = VMStatus.FAILED
            db.commit()
            return {"status": "failed", "message": "VM creation failed randomly"}
        
        # Simulate creation time (30-60 seconds)
        creation_time = random.randint(
            settings.vm_creation_time_min, 
            settings.vm_creation_time_max
        )
        
        # Update progress
        for i in range(creation_time):
            time.sleep(1)
            progress = (i + 1) / creation_time * 100
            self.update_state(
                state="PROGRESS",
                meta={"current": i + 1, "total": creation_time, "progress": progress}
            )
        
        # Generate random IP address in 10.0.0.0/16 range
        ip_parts = [10, 0, random.randint(0, 255), random.randint(1, 254)]
        ip_address = ".".join(map(str, ip_parts))
        
        # Update VM status
        vm.resource_status = ResourceStatus.ACTIVE
        vm.status = VMStatus.RUNNING
        vm.ip_address = ip_address
        db.commit()
        
        return {
            "status": "success",
            "message": "VM created successfully",
            "ip_address": ip_address
        }
        
    except Exception as e:
        if vm:
            vm.resource_status = ResourceStatus.FAILED
            vm.status = VMStatus.FAILED
            db.commit()
        return {"status": "failed", "message": str(e)}
    finally:
        db.close()

@celery_app.task(bind=True)
def create_volume_task(self, volume_data: dict):
    """Create volume task with random failure and timing"""
    db = get_db_session()
    
    try:
        # Check if volume exists
        volume = db.query(Volume).filter(Volume.id == volume_data["id"]).first()
        if not volume:
            return {"status": "failed", "message": "Volume not found"}
        
        # Update status to creating
        volume.resource_status = ResourceStatus.CREATING
        volume.status = VolumeStatus.CREATING
        db.commit()
        
        # Simulate random failure (1/10 chance)
        if random.random() < settings.worker_failure_rate:
            volume.resource_status = ResourceStatus.FAILED
            volume.status = VolumeStatus.FAILED
            db.commit()
            return {"status": "failed", "message": "Volume creation failed randomly"}
        
        # Simulate creation time (30-60 seconds)
        creation_time = random.randint(
            settings.volume_creation_time_min, 
            settings.volume_creation_time_max
        )
        
        # Update progress
        for i in range(creation_time):
            time.sleep(1)
            progress = (i + 1) / creation_time * 100
            self.update_state(
                state="PROGRESS",
                meta={"current": i + 1, "total": creation_time, "progress": progress}
            )
        
        # Update volume status
        volume.resource_status = ResourceStatus.ACTIVE
        volume.status = VolumeStatus.AVAILABLE
        db.commit()
        
        return {
            "status": "success",
            "message": "Volume created successfully"
        }
        
    except Exception as e:
        if volume:
            volume.resource_status = ResourceStatus.FAILED
            volume.status = VolumeStatus.FAILED
            db.commit()
        return {"status": "failed", "message": str(e)}
    finally:
        db.close()

@celery_app.task(bind=True)
def delete_vm_task(self, vm_id: int):
    """Delete VM task"""
    db = get_db_session()
    
    try:
        vm = db.query(VM).filter(VM.id == vm_id).first()
        if not vm:
            return {"status": "failed", "message": "VM not found"}
        
        vm.resource_status = ResourceStatus.DELETING
        vm.status = VMStatus.DELETING
        db.commit()
        
        # Simulate deletion time
        time.sleep(5)
        
        vm.resource_status = ResourceStatus.DELETED
        vm.status = VMStatus.DELETED
        db.commit()
        
        return {"status": "success", "message": "VM deleted successfully"}
        
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    finally:
        db.close()

@celery_app.task(bind=True)
def delete_volume_task(self, volume_id: int):
    """Delete volume task"""
    db = get_db_session()
    
    try:
        volume = db.query(Volume).filter(Volume.id == volume_id).first()
        if not volume:
            return {"status": "failed", "message": "Volume not found"}
        
        volume.resource_status = ResourceStatus.DELETING
        volume.status = VolumeStatus.DELETING
        db.commit()
        
        # Simulate deletion time
        time.sleep(5)
        
        volume.resource_status = ResourceStatus.DELETED
        volume.status = VolumeStatus.DELETED
        db.commit()
        
        return {"status": "success", "message": "Volume deleted successfully"}
        
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    celery_app.start()
