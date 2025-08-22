#!/usr/bin/env python3
"""
Export OpenAPI specification for SDK generation
"""

import json
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

def export_openapi():
    """Export OpenAPI specification to JSON file"""
    
    # Get the OpenAPI specification
    openapi_spec = app.openapi()
    
    # Create output directory if it doesn't exist
    output_dir = Path("openapi")
    output_dir.mkdir(exist_ok=True)
    
    # Export as JSON
    json_file = output_dir / "api.json"
    with open(json_file, "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"✅ OpenAPI specification exported to: {json_file}")
    
    # Export as YAML (optional)
    try:
        import yaml
        yaml_file = output_dir / "api.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(openapi_spec, f, default_flow_style=False, sort_keys=False)
        print(f"✅ OpenAPI specification exported to: {yaml_file}")
    except ImportError:
        print("⚠️  PyYAML not installed, skipping YAML export")
    
    # Print SDK generation instructions
    print("\n🚀 SDK Generation Instructions:")
    print("=" * 50)
    
    print("\n📱 Python SDK (using openapi-generator):")
    print(f"openapi-generator generate -i {json_file} -g python -o sdk/python")
    
    print("\n🐹 Go SDK (using openapi-generator):")
    print(f"openapi-generator generate -i {json_file} -g go -o sdk/go")
    
    print("\n🟢 Node.js SDK (using openapi-generator):")
    print(f"openapi-generator generate -i {json_file} -g javascript -o sdk/nodejs")
    
    print("\n🔧 Alternative: Use swagger-codegen:")
    print(f"swagger-codegen generate -i {json_file} -l python -o sdk/python-swagger")
    print(f"swagger-codegen generate -i {json_file} -l go -o sdk/go-swagger")
    print(f"swagger-codegen generate -i {json_file} -l javascript -o sdk/nodejs-swagger")
    
    print("\n📚 API Documentation:")
    print(f"   - Swagger UI: http://localhost:8000/docs")
    print(f"   - ReDoc: http://localhost:8000/redoc")
    print(f"   - OpenAPI JSON: http://localhost:8000/openapi.json")

if __name__ == "__main__":
    export_openapi()
