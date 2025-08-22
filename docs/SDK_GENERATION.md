# SDK Generation Guide

This guide explains how to generate client SDKs for Python, Go, and Node.js from the Mock Cloud API OpenAPI specification.

## 🚀 Quick Start

### 1. Export OpenAPI Specification

```bash
# From the project root
python scripts/export_openapi.py
```

This will create:
- `openapi/api.json` - OpenAPI specification in JSON format
- `openapi/api.yaml` - OpenAPI specification in YAML format

### 2. Generate SDKs

#### Option A: Using OpenAPI Generator (Recommended)

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python SDK
openapi-generator generate -i openapi/api.json -g python -o sdk/python

# Generate Go SDK
openapi-generator generate -i openapi/api.json -g go -o sdk/go

# Generate Node.js SDK
openapi-generator generate -i openapi/api.json -g javascript -o sdk/nodejs
```

#### Option B: Using Swagger Codegen

```bash
# Install Swagger Codegen
npm install -g swagger-codegen

# Generate Python SDK
swagger-codegen generate -i openapi/api.json -l python -o sdk/python-swagger

# Generate Go SDK
swagger-codegen generate -i openapi/api.json -l go -o sdk/go-swagger

# Generate Node.js SDK
swagger-codegen generate -i openapi/api.json -l javascript -o sdk/nodejs-swagger
```

## 📱 Python SDK

### Installation
```bash
cd sdk/python
pip install -e .
```

### Usage Example
```python
import mock_cloud_api
from mock_cloud_api.rest import ApiException

# Configure API client
configuration = mock_cloud_api.Configuration(
    host="http://localhost:8000"
)

# Create API client
api_client = mock_cloud_api.ApiClient(configuration)

# Create environment
env_api = mock_cloud_api.EnvironmentsApi(api_client)
try:
    env = env_api.create_environment({
        "name": "prod-web",
        "network_cidr": "10.100.0.0/16",
        "description": "Production web environment"
    })
    print(f"Environment created: {env.id}")
except ApiException as e:
    print(f"Error: {e}")
```

## 🐹 Go SDK

### Installation
```bash
cd sdk/go
go mod init mock-cloud-api
go mod tidy
```

### Usage Example
```go
package main

import (
    "fmt"
    "log"
    "github.com/mock-cloud/mock-cloud-api-go"
)

func main() {
    // Configure API client
    config := mock_cloud_api.NewConfiguration()
    config.Servers = []mock_cloud_api.ServerConfiguration{
        {
            URL: "http://localhost:8000",
        },
    }

    // Create API client
    client := mock_cloud_api.NewAPIClient(config)

    // Create environment
    env, resp, err := client.EnvironmentsApi.CreateEnvironment(context.Background()).
        EnvironmentCreate(mock_cloud_api.EnvironmentCreate{
            Name:        "prod-web",
            NetworkCidr: "10.100.0.0/16",
            Description: "Production web environment",
        }).Execute()

    if err != nil {
        log.Fatalf("Error creating environment: %v", err)
    }

    fmt.Printf("Environment created: %d\n", env.Id)
}
```

## 🟢 Node.js SDK

### Installation
```bash
cd sdk/nodejs
npm install
```

### Usage Example
```javascript
const MockCloudApi = require('@mock-cloud/mock-cloud-api');

// Configure API client
const api = new MockCloudApi.DefaultApi({
    basePath: 'http://localhost:8000'
});

// Create environment
const environmentData = {
    name: 'prod-web',
    network_cidr: '10.100.0.0/16',
    description: 'Production web environment'
};

api.createEnvironment(environmentData)
    .then(response => {
        console.log(`Environment created: ${response.data.id}`);
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

## 🔧 Terraform Provider Development

The Mock Cloud API is designed to work seamlessly with Terraform providers:

### Key Features for Terraform
- **Resource IDs**: All resources return IDs immediately
- **Async Operations**: Task IDs for monitoring long-running operations
- **Error Handling**: Structured errors for provider logic
- **State Management**: Consistent resource state representation

### Example Terraform Resource
```hcl
resource "mockcloud_environment" "prod" {
  name         = "prod-web"
  network_cidr = "10.100.0.0/16"
  description  = "Production web environment"
}

resource "mockcloud_vm" "web_server" {
  name           = "web-server-01"
  instance_type  = "t3.micro"
  environment_id = mockcloud_environment.prod.id
  
  depends_on = [mockcloud_environment.prod]
}
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

#### Environments
- `POST /api/v1/environments/` - Create environment
- `GET /api/v1/environments/{id}` - Get environment
- `GET /api/v1/environments/` - List environments
- `DELETE /api/v1/environments/{id}` - Delete environment

#### Virtual Machines
- `POST /api/v1/vms/` - Create VM
- `GET /api/v1/vms/{id}` - Get VM
- `GET /api/v1/vms/` - List VMs
- `DELETE /api/v1/vms/{id}` - Delete VM

#### Volumes
- `POST /api/v1/volumes/` - Create volume
- `GET /api/v1/volumes/{id}` - Get volume
- `GET /api/v1/volumes/` - List volumes
- `DELETE /api/v1/volumes/{id}` - Delete volume
- `POST /api/v1/volumes/{id}/attach` - Attach to VM
- `POST /api/v1/volumes/{id}/detach` - Detach from VM

#### Security Groups
- `POST /api/v1/security-groups/` - Create security group
- `GET /api/v1/security-groups/{id}` - Get security group
- `GET /api/v1/security-groups/` - List security groups
- `DELETE /api/v1/security-groups/{id}` - Delete security group

## 🛠️ Customization

### OpenAPI Generator Options

```bash
# Custom Python package name
openapi-generator generate \
  -i openapi/api.json \
  -g python \
  -o sdk/python \
  --package-name mockcloud \
  --package-version 1.0.0

# Custom Go module name
openapi-generator generate \
  -i openapi/api.json \
  -g go \
  -o sdk/go \
  --package-name github.com/your-org/mock-cloud-api-go

# Custom Node.js package name
openapi-generator generate \
  -i openapi/api.json \
  -g javascript \
  -o sdk/nodejs \
  --package-name @your-org/mock-cloud-api
```

### Configuration Files
You can create configuration files for consistent SDK generation:

```yaml
# config.yaml
packageName: mockcloud
packageVersion: 1.0.0
packageUrl: https://github.com/your-org/mock-cloud-api
infoEmail: support@mockcloud.local
licenseName: MIT
licenseUrl: https://opensource.org/licenses/MIT
```

## 🧪 Testing Generated SDKs

### Python Testing
```bash
cd sdk/python
python -m pytest tests/
```

### Go Testing
```bash
cd sdk/go
go test ./...
```

### Node.js Testing
```bash
cd sdk/nodejs
npm test
```

## 📖 Best Practices

1. **Version Control**: Commit generated SDKs to version control
2. **CI/CD Integration**: Automate SDK generation in your pipeline
3. **Documentation**: Maintain SDK-specific documentation
4. **Testing**: Write tests for your SDK usage
5. **Error Handling**: Implement proper error handling in client code

## 🆘 Troubleshooting

### Common Issues

1. **OpenAPI Generator Not Found**
   ```bash
   npm install -g @openapitools/openapi-generator-cli
   ```

2. **Permission Denied**
   ```bash
   sudo npm install -g @openapitools/openapi-generator-cli
   ```

3. **Invalid OpenAPI Spec**
   - Check the API is running: `curl http://localhost:8000/openapi.json`
   - Validate the spec: Use online OpenAPI validator

4. **SDK Generation Fails**
   - Check OpenAPI generator version compatibility
   - Review the generated error logs
   - Ensure all required dependencies are installed

## 🔗 Additional Resources

- [OpenAPI Generator Documentation](https://openapi-generator.tech/)
- [Swagger Codegen Documentation](https://swagger.io/tools/swagger-codegen/)
- [FastAPI OpenAPI Documentation](https://fastapi.tiangolo.com/advanced/openapi/)
- [Terraform Provider Development](https://www.terraform.io/docs/extend/developing.html)
