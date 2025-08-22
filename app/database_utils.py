"""
Database utility functions with error handling
"""

import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, OperationalError
from sqlalchemy.orm import Session
from typing import Any, Optional, TypeVar, Generic, Type
from app.exceptions import (
    DatabaseException, 
    ResourceNotFoundException, 
    ResourceAlreadyExistsException,
    ValidationException
)

logger = logging.getLogger(__name__)

T = TypeVar('T')


def safe_db_operation(operation: str):
    """Decorator to safely handle database operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IntegrityError as e:
                logger.error(f"Database integrity error during {operation}: {e}")
                if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                    raise ResourceAlreadyExistsException(
                        resource_type="resource",
                        resource_name="unknown",
                        detail="Resource already exists with the same unique identifier"
                    )
                raise DatabaseException(operation=operation, detail="Data integrity constraint violated")
            except DataError as e:
                logger.error(f"Database data error during {operation}: {e}")
                raise ValidationException(detail="Invalid data provided", field="data")
            except OperationalError as e:
                logger.error(f"Database operational error during {operation}: {e}")
                raise DatabaseException(operation=operation, detail="Database operation failed")
            except SQLAlchemyError as e:
                logger.error(f"Database error during {operation}: {e}")
                raise DatabaseException(operation=operation, detail="Database operation failed")
            except Exception as e:
                logger.error(f"Unexpected error during {operation}: {e}")
                raise DatabaseException(operation=operation, detail="Unexpected database error")
        return wrapper
    return decorator


def get_resource_by_id(
    db: Session, 
    model: Type[T], 
    resource_id: int, 
    resource_type: str
) -> T:
    """Safely get a resource by ID with proper error handling"""
    
    @safe_db_operation(f"get {resource_type}")
    def _get_resource():
        resource = db.query(model).filter(model.id == resource_id).first()
        if not resource:
            raise ResourceNotFoundException(
                resource_type=resource_type,
                resource_id=str(resource_id)
            )
        return resource
    
    return _get_resource()


def create_resource(
    db: Session, 
    model: Type[T], 
    data: dict, 
    resource_type: str
) -> T:
    """Safely create a resource with proper error handling"""
    
    @safe_db_operation(f"create {resource_type}")
    def _create_resource():
        try:
            db_resource = model(**data)
            db.add(db_resource)
            db.commit()
            db.refresh(db_resource)
            return db_resource
        except Exception as e:
            db.rollback()
            raise e
    
    return _create_resource()


def update_resource(
    db: Session, 
    model: Type[T], 
    resource_id: int, 
    data: dict, 
    resource_type: str
) -> T:
    """Safely update a resource with proper error handling"""
    
    @safe_db_operation(f"update {resource_type}")
    def _update_resource():
        resource = get_resource_by_id(db, model, resource_id, resource_type)
        
        for field, value in data.items():
            if hasattr(resource, field):
                setattr(resource, field, value)
        
        db.commit()
        db.refresh(resource)
        return resource
    
    return _update_resource()


def delete_resource(
    db: Session, 
    model: Type[T], 
    resource_id: int, 
    resource_type: str
) -> bool:
    """Safely delete a resource with proper error handling"""
    
    @safe_db_operation(f"delete {resource_type}")
    def _delete_resource():
        resource = get_resource_by_id(db, model, resource_id, resource_type)
        db.delete(resource)
        db.commit()
        return True
    
    return _delete_resource()


def list_resources(
    db: Session, 
    model: Type[T], 
    skip: int = 0, 
    limit: int = 100,
    filters: Optional[dict] = None
) -> tuple[list[T], int]:
    """Safely list resources with proper error handling"""
    
    @safe_db_operation(f"list {model.__name__.lower()}")
    def _list_resources():
        query = db.query(model)
        
        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                if hasattr(model, field):
                    query = query.filter(getattr(model, field) == value)
        
        total = query.count()
        resources = query.offset(skip).limit(limit).all()
        
        return resources, total
    
    return _list_resources()


def check_resource_exists(
    db: Session, 
    model: Type[T], 
    field: str, 
    value: Any, 
    resource_type: str
) -> bool:
    """Check if a resource exists with a specific field value"""
    
    @safe_db_operation(f"check {resource_type} exists")
    def _check_exists():
        return db.query(model).filter(getattr(model, field) == value).first() is not None
    
    return _check_exists()


def safe_commit(db: Session, operation: str = "database operation"):
    """Safely commit database changes with rollback on error"""
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to commit {operation}: {e}")
        raise DatabaseException(operation=operation, detail="Failed to save changes")
