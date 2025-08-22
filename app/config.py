import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://mockcloud:mockcloud123@localhost:5432/mockcloud"
    
    # RabbitMQ
    rabbitmq_url: str = "amqp://mockcloud:mockcloud123@localhost:5672/"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Celery
    celery_broker_url: str = "amqp://mockcloud:mockcloud123@localhost:5672/"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Worker Settings
    worker_failure_rate: float = 0.1  # 1/10 chance of failure
    vm_creation_time_min: int = 30   # seconds
    vm_creation_time_max: int = 60   # seconds
    volume_creation_time_min: int = 30  # seconds
    volume_creation_time_max: int = 60  # seconds
    
    class Config:
        env_file = ".env"

settings = Settings()
