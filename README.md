# Mock Cloud API

A mock cloud backend API built with FastAPI, featuring VM and volume management, security groups, and environments. The system uses Celery workers with RabbitMQ for asynchronous task processing, simulating real cloud infrastructure operations.

## Features

- **Virtual Machines (VMs)**: Create, delete, and manage VMs with realistic timing
- **Volumes**: Block storage management with attach/detach capabilities
- **Security Groups**: Network security configuration
- **Environments**: Network isolation with 10.0.0.0/16 CIDR ranges
- **Asynchronous Processing**: Celery workers with RabbitMQ for resource creation
- **Realistic Simulation**: 30-60 second creation times with 1/10 failure rate
- **PostgreSQL Database**: Persistent storage for all resources
- **Redis**: Celery result backend and caching

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │    │   Celery    │    │ PostgreSQL  │
│     API     │◄──►│   Worker    │◄──►│  Database   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │
       │                   │
       ▼                   ▼
┌─────────────┐    ┌─────────────┐
│  RabbitMQ   │    │    Redis    │
│   Broker    │    │   Backend   │
└─────────────┘    └─────────────┘
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 15
- RabbitMQ 3
- Redis 7

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd mock-cloud-api
```

### 2. Environment Configuration

Copy the example environment file and modify as needed:

```bash
cp env.example .env
# Edit .env with your configuration
```

### 3. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- RabbitMQ on port 5672 (Management UI on 15672)
- Redis on port 6379
- FastAPI application on port 8000
- Celery worker

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Environments
- `POST /api/v1/environments/` - Create environment
- `GET /api/v1/environments/` - List all environments
- `GET /api/v1/environments/{id}` - Get environment by ID
- `DELETE /api/v1/environments/{id}` - Delete environment

### Security Groups
- `POST /api/v1/security-groups/` - Create security group
- `GET /api/v1/security-groups/` - List all security groups
- `GET /api/v1/security-groups/{id}` - Get security group by ID
- `DELETE /api/v1/security-groups/{id}` - Delete security group

### Virtual Machines
- `POST /api/v1/vms/` - Create VM (asynchronous)
- `GET /api/v1/vms/` - List all VMs
- `GET /api/v1/vms/{id}` - Get VM by ID
- `DELETE /api/v1/vms/{id}` - Delete VM (asynchronous)

### Volumes
- `POST /api/v1/volumes/` - Create volume (asynchronous)
- `GET /api/v1/volumes/` - List all volumes
- `GET /api/v1/volumes/{id}` - Get volume by ID
- `DELETE /api/v1/volumes/{id}` - Delete volume (asynchronous)
- `POST /api/v1/volumes/{id}/attach/{vm_id}` - Attach volume to VM
- `POST /api/v1/volumes/{id}/detach` - Detach volume from VM

## Worker Behavior

The Celery worker simulates realistic cloud operations:

- **VM Creation**: 30-60 seconds with 1/10 failure rate
- **Volume Creation**: 30-60 seconds with 1/10 failure rate
- **Resource Status Updates**: Real-time progress tracking
- **IP Assignment**: Random IP addresses in 10.0.0.0/16 range
- **Failure Simulation**: Random failures to test error handling

## Development

### Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start services** (using Docker Compose):
   ```bash
   docker-compose up -d postgres rabbitmq redis
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Start the worker** (in another terminal):
   ```bash
   celery -A app.worker.celery_app worker --loglevel=info
   ```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Configuration

Key configuration options in `app/config.py`:

- `worker_failure_rate`: Probability of resource creation failure (default: 0.1)
- `vm_creation_time_min/max`: VM creation time range in seconds
- `volume_creation_time_min/max`: Volume creation time range in seconds

## Monitoring

- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Database**: Connect to PostgreSQL on localhost:5432
- **Worker Logs**: Check Celery worker output for task progress

## Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Ensure PostgreSQL is running and accessible
   - Check database credentials in `.env`

2. **Worker Not Processing Tasks**:
   - Verify RabbitMQ is running
   - Check Celery worker logs for errors
   - Ensure Redis is accessible

3. **API Not Starting**:
   - Check if port 8000 is available
   - Verify all dependencies are installed
   - Check application logs for errors

### Logs

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs worker
docker-compose logs postgres
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
