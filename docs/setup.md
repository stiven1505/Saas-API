# Setup Instructions

## Prerequisites

### System Requirements
- Python 3.11 or higher
- Node.js 20 or higher
- Docker & Docker Compose (optional but recommended)
- PostgreSQL 16 (only if not using Docker)
- Git


## Installation

### Option 1: Using Docker Compose (Recommended)

This is the easiest way to get the entire stack running.

```bash
# 1. Clone the repository
git clone <repository-url>
cd SaaS

# 2. Create .env file
cp .env.example .env

# 3. Update .env with your API keys
# Edit .env and add:
# - GEMINI_API_KEY=your-key-here

# 4. Start all services
docker-compose up --build

# 5. Access applications
# Frontend: http://localhost:4200
# Backend API: http://localhost:8000/docs (Swagger)
# Database: postgres://postgres:postgres@localhost:5432/saas_db
```

### Option 2: Local Development Setup

#### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Update .env with your configuration
# Ensure DATABASE_URL points to your PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/saas_db

# 7. Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Frontend will open at http://localhost:4200
```

#### Database Setup (Local)

```bash
# 1. Install PostgreSQL 16
# macOS: brew install postgresql@16
# Ubuntu: sudo apt install postgresql-16
# Windows: Download installer from postgresql.org

# 2. Start PostgreSQL
# macOS: brew services start postgresql@16
# Ubuntu: sudo systemctl start postgresql
# Windows: Use Services app

# 3. Create database
createdb -U postgres saas_db

# 4. Run migrations (when implemented)
cd backend
alembic upgrade head
```

## Verification

### Backend Health Check

```bash
# Test API is running
curl http://localhost:8000/health

# Should return:
# {"status":"ok"}

# Access Swagger documentation
# Open: http://localhost:8000/docs
```

### Frontend Health Check

```bash
# Frontend should be running at:
# http://localhost:4200

# You should see the login page
```

### Database Health Check

```bash
# Connect to database
psql -U postgres -h localhost saas_db

# List tables
\dt

# Exit
\q
```

## Test Credentials

Use these credentials to test the application after seeding:

```
Email: test@example.com
Password: password123
```

## Common Issues & Solutions

### Issue: Database Connection Failed

**Solution:**
```bash
# Check PostgreSQL is running
# macOS: brew services list
# Ubuntu: systemctl status postgresql

# Check connection string in .env
# Ensure DATABASE_URL is correct
```

### Issue: Port Already in Use

**Solution:**
```bash
# Backend (8000)
lsof -i :8000  # Find process
kill -9 <PID>   # Kill process

# Frontend (4200)
lsof -i :4200
kill -9 <PID>

# Docker
docker-compose down  # Stop all services
```

### Issue: Python Module Not Found

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Node Modules Issues

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules

# Reinstall
npm install
```

## Production Deployment

### Using Docker

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Deployment

1. Set up Ubuntu 22.04 LTS server
2. Install Python 3.11, Node.js 20, PostgreSQL 16
3. Clone repository
4. Set up virtual environments
5. Configure environment variables
6. Use systemd services to manage processes
7. Set up Nginx reverse proxy
8. Configure SSL/TLS with Let's Encrypt

### Environment Configuration

```bash
# Production .env example
DATABASE_URL=postgresql+asyncpg://prod_user:strong_password@db.example.com:5432/saas_prod
JWT_SECRET=your-very-long-random-secret-key-here-min-32-chars
JWT_EXPIRE_MINUTES=60
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

## Troubleshooting

### Check Service Status

```bash
# Docker
docker ps

# Backend process
ps aux | grep uvicorn

# Frontend process
ps aux | grep vite
```

### View Logs

```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Local backend
# Logs appear in terminal where uvicorn is running

# Local frontend
# Logs appear in terminal where npm run dev is running
```

### Reset Database

```bash
# WARNING: This will delete all data!

# Drop and recreate database
dropdb saas_db
createdb saas_db

# Rerun migrations
cd backend
alembic upgrade head
```

## Next Steps

1. Review the [Architecture Documentation](./architecture.md)
2. Read the [API Documentation](./api.md)
3. Check the [Development Guide](./development.md)
4. Review [Deployment Guide](./deployment.md)

## Getting Help

- Check existing documentation in `/docs`
- Review code comments
- Check GitHub Issues
- Contact the development team

## Security Reminders

⚠️ **Before Production:**
- Change JWT_SECRET to a strong random value
- Enable DEBUG=false
- Set up HTTPS/SSL
- Configure CORS for production domain
- Use strong database passwords
- Set up regular backups
- Review security configuration
