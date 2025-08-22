"""
Custom exceptions for Mock Cloud API
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class MockCloudException(HTTPException):
    """Base exception for Mock Cloud API"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.resource_type = resource_type
        self.resource_id = resource_id


class ResourceNotFoundException(MockCloudException):
    """Resource not found exception"""
    
    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        detail: Optional[str] = None
    ):
        if not detail:
            detail = f"{resource_type} with id {resource_id} not found"
        
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND",
            resource_type=resource_type,
            resource_id=resource_id
        )


class ResourceAlreadyExistsException(MockCloudException):
    """Resource already exists exception"""
    
    def __init__(
        self,
        resource_type: str,
        resource_name: str,
        detail: Optional[str] = None
    ):
        if not detail:
            detail = f"{resource_type} with name '{resource_name}' already exists"
        
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="RESOURCE_ALREADY_EXISTS",
            resource_type=resource_type
        )


class ValidationException(MockCloudException):
    """Validation exception"""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="VALIDATION_ERROR",
            resource_type=field
        )


class ResourceOperationException(MockCloudException):
    """Resource operation exception"""
    
    def __init__(
        self,
        operation: str,
        resource_type: str,
        resource_id: str,
        detail: Optional[str] = None
    ):
        if not detail:
            detail = f"Failed to {operation} {resource_type} {resource_id}"
        
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="RESOURCE_OPERATION_FAILED",
            resource_type=resource_type,
            resource_id=resource_id
        )


class DatabaseException(MockCloudException):
    """Database operation exception"""
    
    def __init__(self, operation: str, detail: Optional[str] = None):
        if not detail:
            detail = f"Database {operation} failed"
        
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )


class WorkerTaskException(MockCloudException):
    """Worker task exception"""
    
    def __init__(self, task_type: str, detail: Optional[str] = None):
        if not detail:
            detail = f"Worker task {task_type} failed"
        
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="WORKER_TASK_FAILED"
        )


def create_error_response(
    status_code: int,
    detail: str,
    error_code: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a standardized error response"""
    
    error_response = {
        "error": {
            "code": error_code or "UNKNOWN_ERROR",
            "message": detail,
            "status_code": status_code
        }
    }
    
    if resource_type:
        error_response["error"]["resource_type"] = resource_type
    
    if resource_id:
        error_response["error"]["resource_id"] = resource_id
    
    # Add any additional fields
    for key, value in kwargs.items():
        error_response["error"][key] = value
    
    return error_response
