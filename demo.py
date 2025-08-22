#!/usr/bin/env python3
"""
Mock Cloud API Demo Script

This script demonstrates the API functionality and shows how to use
the generated SDKs for programmatic resource management.
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_VERSION = "v1"

class MockCloudAPIClient:
    """Simple client for the Mock Cloud API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}/api/{API_VERSION}/{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return {}
    
    def create_environment(self, name: str, network_cidr: str, description: str = "") -> Dict[str, Any]:
        """Create a new environment"""
        data = {
            "name": name,
            "network_cidr": network_cidr,
            "description": description
        }
        return self._make_request('POST', 'environments/', data)
    
    def get_environment(self, env_id: int) -> Dict[str, Any]:
        """Get environment by ID"""
        return self._make_request('GET', f'environments/{env_id}')
    
    def list_environments(self) -> Dict[str, Any]:
        """List all environments"""
        return self._make_request('GET', 'environments/')
    
    def create_vm(self, name: str, instance_type: str, environment_id: int) -> Dict[str, Any]:
        """Create a new VM"""
        data = {
            "name": name,
            "instance_type": instance_type,
            "environment_id": environment_id
        }
        return self._make_request('POST', 'vms/', data)
    
    def get_vm(self, vm_id: int) -> Dict[str, Any]:
        """Get VM by ID"""
        return self._make_request('GET', f'vms/{vm_id}')
    
    def list_vms(self) -> Dict[str, Any]:
        """List all VMs"""
        return self._make_request('GET', 'vms/')
    
    def create_volume(self, name: str, size_gb: int, environment_id: int) -> Dict[str, Any]:
        """Create a new volume"""
        data = {
            "name": name,
            "size_gb": size_gb,
            "environment_id": environment_id
        }
        return self._make_request('POST', 'volumes/', data)
    
    def get_volume(self, volume_id: int) -> Dict[str, Any]:
        """Get volume by ID"""
        return self._make_request('GET', f'volumes/{volume_id}')
    
    def list_volumes(self) -> Dict[str, Any]:
        """List all volumes"""
        return self._make_request('GET', 'volumes/')
    
    def create_security_group(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new security group"""
        data = {
            "name": name,
            "description": description
        }
        return self._make_request('POST', 'security-groups/', data)
    
    def get_security_group(self, sg_id: int) -> Dict[str, Any]:
        """Get security group by ID"""
        return self._make_request('GET', f'security-groups/{sg_id}')
    
    def list_security_groups(self) -> Dict[str, Any]:
        """List all security groups"""
        return self._make_request('GET', 'security-groups/')

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_resource(title: str, resource: Dict[str, Any]):
    """Print resource information"""
    print(f"\n📋 {title}")
    print(f"   ID: {resource.get('id', 'N/A')}")
    print(f"   Name: {resource.get('name', 'N/A')}")
    print(f"   Status: {resource.get('status', 'N/A')}")
    if 'created_at' in resource:
        print(f"   Created: {resource['created_at']}")
    if 'network_cidr' in resource:
        print(f"   Network: {resource['network_cidr']}")
    if 'instance_type' in resource:
        print(f"   Type: {resource['instance_type']}")
    if 'size_gb' in resource:
        print(f"   Size: {resource['size_gb']} GB")

def demo_api_functionality():
    """Demonstrate the API functionality"""
    
    print_section("🚀 Mock Cloud API Demo")
    print("This demo showcases the Mock Cloud API functionality")
    print("Make sure the API is running at http://localhost:8000")
    
    # Initialize API client
    client = MockCloudAPIClient()
    
    # Test API health
    try:
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ API is healthy and running")
        else:
            print("❌ API health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running at http://localhost:8000")
        return
    
    # Create Environment
    print_section("🌍 Creating Environment")
    env_data = client.create_environment(
        name="demo-env",
        network_cidr="10.200.0.0/16",
        description="Demo environment for testing"
    )
    
    if env_data:
        print_resource("Environment Created", env_data)
        environment_id = env_data['id']
    else:
        print("❌ Failed to create environment")
        return
    
    # Create Security Group
    print_section("🔒 Creating Security Group")
    sg_data = client.create_security_group(
        name="demo-sg",
        description="Demo security group"
    )
    
    if sg_data:
        print_resource("Security Group Created", sg_data)
        security_group_id = sg_data['id']
    else:
        print("❌ Failed to create security group")
        return
    
    # Create VM
    print_section("🖥️  Creating Virtual Machine")
    vm_data = client.create_vm(
        name="demo-vm",
        instance_type="t3.micro",
        environment_id=environment_id
    )
    
    if vm_data:
        print_resource("VM Creation Started", vm_data)
        vm_id = vm_data.get('id')
        task_id = vm_data.get('task_id')
        print(f"   Task ID: {task_id}")
        print("   Note: VM creation is async and takes 30-60 seconds")
    else:
        print("❌ Failed to create VM")
        return
    
    # Create Volume
    print_section("💾 Creating Volume")
    volume_data = client.create_volume(
        name="demo-volume",
        size_gb=20,
        environment_id=environment_id
    )
    
    if volume_data:
        print_resource("Volume Creation Started", volume_data)
        volume_id = volume_data.get('id')
        task_id = volume_data.get('task_id')
        print(f"   Task ID: {task_id}")
        print("   Note: Volume creation is async and takes 30-60 seconds")
    else:
        print("❌ Failed to create volume")
        return
    
    # List Resources
    print_section("📋 Listing Resources")
    
    print("\n🌍 Environments:")
    environments = client.list_environments()
    if environments and 'environments' in environments:
        for env in environments['environments']:
            print(f"   - {env['name']} (ID: {env['id']}) - {env['network_cidr']}")
    
    print("\n🔒 Security Groups:")
    security_groups = client.list_security_groups()
    if security_groups and 'security_groups' in security_groups:
        for sg in security_groups['security_groups']:
            print(f"   - {sg['name']} (ID: {sg['id']}) - {sg['description']}")
    
    print("\n🖥️  Virtual Machines:")
    vms = client.list_vms()
    if vms and 'vms' in vms:
        for vm in vms['vms']:
            print(f"   - {vm['name']} (ID: {vm['id']}) - {vm['status']} - {vm['instance_type']}")
    
    print("\n💾 Volumes:")
    volumes = client.list_volumes()
    if volumes and 'volumes' in volumes:
        for volume in volumes['volumes']:
            print(f"   - {volume['name']} (ID: {volume['id']}) - {volume['status']} - {volume['size_gb']} GB")
    
    # SDK Generation Info
    print_section("🔧 SDK Generation")
    print("To generate SDKs for Python, Go, and Node.js:")
    print("\n1. Export OpenAPI specification:")
    print("   python scripts/export_openapi.py")
    print("\n2. Generate SDKs:")
    print("   make generate-all-sdks")
    print("\n3. Or generate individually:")
    print("   make generate-sdk-python")
    print("   make generate-sdk-go")
    print("   make generate-sdk-nodejs")
    
    print("\n📚 API Documentation:")
    print(f"   - Swagger UI: {API_BASE_URL}/docs")
    print(f"   - ReDoc: {API_BASE_URL}/redoc")
    print(f"   - OpenAPI JSON: {API_BASE_URL}/openapi.json")
    
    print("\n🎯 Next Steps:")
    print("   1. Wait for VM and Volume creation to complete")
    print("   2. Generate SDKs using the commands above")
    print("   3. Build your Terraform provider")
    print("   4. Integrate with your CI/CD pipelines")

if __name__ == "__main__":
    demo_api_functionality()
