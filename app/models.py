from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class ResourceStatus(str, enum.Enum):
    PENDING = "pending"
    CREATING = "creating"
    ACTIVE = "active"
    FAILED = "failed"
    DELETING = "deleting"
    DELETED = "deleted"

class VMStatus(str, enum.Enum):
    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    DELETING = "deleting"
    DELETED = "deleted"

class VolumeStatus(str, enum.Enum):
    PENDING = "pending"
    CREATING = "creating"
    AVAILABLE = "available"
    IN_USE = "in_use"
    FAILED = "failed"
    DELETING = "deleting"
    DELETED = "deleted"

class Environment(Base):
    __tablename__ = "environments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    network_cidr = Column(String(18), default="10.0.0.0/16")
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    vms = relationship("VM", back_populates="environment")
    volumes = relationship("Volume", back_populates="environment")

class SecurityGroup(Base):
    __tablename__ = "security_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    rules = Column(Text)  # JSON string of security rules
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    vms = relationship("VM", back_populates="security_group")

class VM(Base):
    __tablename__ = "vms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    instance_type = Column(String(50), nullable=False)
    status = Column(Enum(VMStatus), default=VMStatus.PENDING)
    resource_status = Column(Enum(ResourceStatus), default=ResourceStatus.PENDING)
    ip_address = Column(String(15))
    environment_id = Column(Integer, ForeignKey("environments.id"))
    security_group_id = Column(Integer, ForeignKey("security_groups.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    environment = relationship("Environment", back_populates="vms")
    security_group = relationship("SecurityGroup", back_populates="vms")
    volumes = relationship("Volume", back_populates="vm")

class Volume(Base):
    __tablename__ = "volumes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    size_gb = Column(Integer, nullable=False)
    status = Column(Enum(VolumeStatus), default=VolumeStatus.PENDING)
    resource_status = Column(Enum(ResourceStatus), default=ResourceStatus.PENDING)
    environment_id = Column(Integer, ForeignKey("environments.id"))
    vm_id = Column(Integer, ForeignKey("vms.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    environment = relationship("Environment", back_populates="volumes")
    vm = relationship("VM", back_populates="volumes")
