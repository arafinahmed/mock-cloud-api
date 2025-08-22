"""
Basic tests for Mock Cloud API
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Mock Cloud API" in response.json()["message"]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_docs_endpoint():
    """Test that API docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_endpoint():
    """Test that ReDoc is accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200
