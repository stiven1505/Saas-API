#!/bin/bash

# Quick Start Script for SaaS Platform
# This script sets up and starts the entire application

set -e

echo "🚀 SaaS Platform - Quick Start"
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys before proceeding"
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:4200"
echo "   API Docs:  http://localhost:8000/docs"
echo "   API Health: http://localhost:8000/health"
echo "   Database: postgres://postgres:postgres@localhost:5432/saas_db"
echo ""
echo "📝 Test Credentials:"
echo "   Email: test@example.com"
echo "   Password: password123"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Project overview"
echo "   - docs/setup.md - Detailed setup instructions"
echo "   - docs/architecture.md - Architecture documentation"
echo "   - docs/api.md - API endpoints"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "📊 To view logs: docker-compose logs -f backend"
