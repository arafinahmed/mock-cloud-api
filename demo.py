#!/usr/bin/env python3
"""
Demo script for Mock Cloud API
Creates sample resources and demonstrates the API functionality
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000/api/v1"

def wait_for_service():
    """Wait for the API service to be ready"""
    print("⏳ Waiting for API service to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
            if response.status_code == 200:
                print("✅ API service is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        if attempt < max_attempts - 1:
            time.sleep(2)
            print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print("❌ API service is not responding")
    return False

def create_environment(name, network_cidr, description):
    """Create an environment"""
    data = {
        "name": name,
        "network_cidr": network_cidr,
        "description": description
    }
    
    response = requests.post(f"{BASE_URL}/environments/", json=data)
    if response.status_code == 201:
        print(f"✅ Created environment: {name}")
        return response.json()
    else:
        print(f"❌ Failed to create environment {name}: {response.text}")
        return None

def create_security_group(name, description, rules):
    """Create a security group"""
    data = {
        "name": name,
        "description": description,
        "rules": json.dumps(rules)
    }
    
    response = requests.post(f"{BASE_URL}/security-groups/", json=data)
    if response.status_code == 201:
        print(f"✅ Created security group: {name}")
        return response.json()
    else:
        print(f"❌ Failed to create security group {name}: {response.text}")
        return None

def create_vm(name, instance_type, environment_id, security_group_id):
    """Create a VM"""
    data = {
        "name": name,
        "instance_type": instance_type,
        "environment_id": environment_id,
        "security_group_id": security_group_id
    }
    
    response = requests.post(f"{BASE_URL}/vms/", json=data)
    if response.status_code == 200:
        print(f"✅ Started VM creation: {name} (Task ID: {response.json()['task_id']})")
        return response.json()
    else:
        print(f"❌ Failed to start VM creation {name}: {response.text}")
        return None

def create_volume(name, size_gb, environment_id):
    """Create a volume"""
    data = {
        "name": name,
        "size_gb": size_gb,
        "environment_id": environment_id
    }
    
    response = requests.post(f"{BASE_URL}/volumes/", json=data)
    if response.status_code == 200:
        print(f"✅ Started volume creation: {name} (Task ID: {response.json()['task_id']})")
        return response.json()
    else:
        print(f"❌ Failed to start volume creation {name}: {response.text}")
        return None

def list_resources():
    """List all resources"""
    print("\n📋 Current Resources:")
    
    # List environments
    response = requests.get(f"{BASE_URL}/environments/")
    if response.status_code == 200:
        envs = response.json()
        print(f"   Environments: {envs['total']}")
        for env in envs['environments']:
            print(f"     - {env['name']} ({env['network_cidr']})")
    
    # List security groups
    response = requests.get(f"{BASE_URL}/security-groups/")
    if response.status_code == 200:
        sgs = response.json()
        print(f"   Security Groups: {sgs['total']}")
        for sg in sgs['security_groups']:
            print(f"     - {sg['name']}")
    
    # List VMs
    response = requests.get(f"{BASE_URL}/vms/")
    if response.status_code == 200:
        vms = response.json()
        print(f"   VMs: {vms['total']}")
        for vm in vms['vms']:
            print(f"     - {vm['name']} ({vm['status']}) - {vm['resource_status']}")
    
    # List volumes
    response = requests.get(f"{BASE_URL}/volumes/")
    if response.status_code == 200:
        volumes = response.json()
        print(f"   Volumes: {volumes['total']}")
        for volume in volumes['volumes']:
            print(f"     - {volume['name']} ({volume['status']}) - {volume['resource_status']}")

def main():
    """Main demo function"""
    print("🚀 Mock Cloud API Demo")
    print("=" * 50)
    
    # Wait for service to be ready
    if not wait_for_service():
        return
    
    print("\n🔧 Creating sample resources...")
    
    # Create environments
    env1 = create_environment("demo-env", "10.100.0.0/16", "Demo environment for testing")
    env2 = create_environment("test-env", "10.101.0.0/16", "Test environment")
    
    if not env1:
        print("❌ Cannot continue without environment")
        return
    
    # Create security groups
    sg1 = create_security_group("demo-sg", "Demo security group", {
        "inbound": [
            {"protocol": "tcp", "port": 22, "source": "0.0.0.0/0"},
            {"protocol": "tcp", "port": 80, "source": "0.0.0.0/0"}
        ],
        "outbound": [
            {"protocol": "all", "port": "all", "destination": "0.0.0.0/0"}
        ]
    })
    
    sg2 = create_security_group("web-sg", "Web server security group", {
        "inbound": [
            {"protocol": "tcp", "port": 80, "source": "0.0.0.0/0"},
            {"protocol": "tcp", "port": 443, "source": "0.0.0.0/0"}
        ],
        "outbound": [
            {"protocol": "all", "port": "all", "destination": "0.0.0.0/0"}
        ]
    })
    
    if not sg1:
        print("❌ Cannot continue without security group")
        return
    
    # Create VMs
    vm1 = create_vm("demo-vm-1", "t3.micro", env1["id"], sg1["id"])
    vm2 = create_vm("demo-vm-2", "t3.small", env1["id"], sg2["id"])
    vm3 = create_vm("test-vm", "t3.medium", env2["id"] if env2 else env1["id"], sg1["id"])
    
    # Create volumes
    vol1 = create_volume("demo-vol-1", 20, env1["id"])
    vol2 = create_volume("demo-vol-2", 50, env1["id"])
    vol3 = create_volume("test-vol", 100, env2["id"] if env2 else env1["id"])
    
    print("\n⏳ Waiting for resources to be created...")
    print("   (This may take 30-60 seconds per resource)")
    
    # Wait a bit and then show current status
    time.sleep(5)
    list_resources()
    
    print("\n🎉 Demo completed!")
    print("\n💡 Tips:")
    print("   - Check the API docs at http://localhost:8000/docs")
    print("   - Monitor worker logs: docker-compose logs -f worker")
    print("   - Some resources may fail randomly (1/10 chance)")
    print("   - Resource creation takes 30-60 seconds")

if __name__ == "__main__":
    main()
