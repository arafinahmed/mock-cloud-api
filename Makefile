.PHONY: help build up down logs clean test migrate init-db

help: ## Show this help message
	@echo "Mock Cloud API - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

logs-api: ## Show API logs
	docker-compose logs -f api

logs-worker: ## Show worker logs
	docker-compose logs -f worker

logs-db: ## Show database logs
	docker-compose logs -f postgres

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

test: ## Run tests
	pytest

migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="description")
	docker-compose exec api alembic revision --autogenerate -m "$(MESSAGE)"

init-db: ## Initialize database with sample data
	docker-compose exec api python scripts/init_db.py

setup: ## Complete setup: start services, run migrations, and initialize DB
	@echo "🚀 Setting up Mock Cloud API..."
	@echo "📦 Building and starting services..."
	@make build
	@make up
	@echo "⏳ Waiting for services to be ready..."
	@sleep 20
	@echo "🔄 Running database migrations..."
	@make migrate
	@echo "📊 Initializing database with sample data..."
	@make init-db
	@echo "✅ Setup complete! API is ready at http://localhost:8000"

start-api: ## Start API locally (requires services to be running)
	uvicorn app.main:app --reload

start-worker: ## Start worker locally (requires services to be running)
	python scripts/start_worker.py

dev-setup: ## Setup development environment
	pip install -r requirements.txt
	docker-compose up -d postgres rabbitmq redis
	alembic upgrade head
	python scripts/init_db.py

status: ## Show service status
	docker-compose ps

# SDK Generation
export-openapi: ## Export OpenAPI specification
	python scripts/export_openapi.py

generate-sdk-python: ## Generate Python SDK
	@echo "Generating Python SDK..."
	@mkdir -p sdk
	openapi-generator generate -i openapi/api.json -g python -o sdk/python --package-name mockcloud

generate-sdk-go: ## Generate Go SDK
	@echo "Generating Go SDK..."
	@mkdir -p sdk
	openapi-generator generate -i openapi/api.json -g go -o sdk/go --package-name github.com/mock-cloud/mock-cloud-api-go

generate-sdk-nodejs: ## Generate Node.js SDK
	@echo "Generating Node.js SDK..."
	@mkdir -p sdk
	openapi-generator generate -i openapi/api.json -g javascript -o sdk/nodejs --package-name @mock-cloud/mock-cloud-api

generate-all-sdks: export-openapi generate-sdk-python generate-sdk-go generate-sdk-nodejs ## Generate all SDKs
	@echo "All SDKs generated successfully!"
	@echo "Python SDK: sdk/python/"
	@echo "Go SDK: sdk/go/"
	@echo "Node.js SDK: sdk/nodejs/"

install-openapi-generator: ## Install OpenAPI Generator CLI
	npm install -g @openapitools/openapi-generator-cli
