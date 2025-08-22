#!/bin/bash

echo "🚀 Starting Mock Cloud API..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo "🔧 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check if database is ready
echo "🗄️  Checking database connection..."
max_attempts=30
for attempt in $(seq 1 $max_attempts); do
    if docker-compose exec -T postgres pg_isready -U mockcloud > /dev/null 2>&1; then
        echo "✅ Database is ready!"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ Database is not responding after $max_attempts attempts"
        exit 1
    fi
    
    echo "   Attempt $attempt/$max_attempts..."
    sleep 2
done

# Run database migrations
echo "🔄 Running database migrations..."
docker-compose exec -T api python scripts/migrate_db.py

# Initialize database with sample data
echo "📊 Initializing database with sample data..."
docker-compose exec -T api python scripts/init_db.py

# Check service status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "✅ Mock Cloud API is ready!"
echo ""
echo "🌐 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "🐰 RabbitMQ Management: http://localhost:15672 (mockcloud/mockcloud123)"
echo "🗄️  PostgreSQL: localhost:5432 (mockcloud/mockcloud123)"
echo "🔴 Redis: localhost:6379"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
