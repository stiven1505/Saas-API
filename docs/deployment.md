# Deployment Guide

## Production Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] Monitoring setup
- [ ] Error tracking (Sentry) configured
- [ ] Logging configured
- [ ] SSL/TLS certificates ready
- [ ] Domain DNS configured
- [ ] CDN configured (optional)

## Docker Deployment

### Build Production Images

```bash
# Build both images
docker-compose build

# Tag images
docker tag saas_backend:latest myregistry/saas-backend:1.0.0
docker tag saas_frontend:latest myregistry/saas-frontend:1.0.0

# Push to registry
docker push myregistry/saas-backend:1.0.0
docker push myregistry/saas-frontend:1.0.0
```

### Deploy to Production

```bash
# Pull latest images
docker pull myregistry/saas-backend:1.0.0
docker pull myregistry/saas-frontend:1.0.0

# Start with production settings
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f backend
```

### Production docker-compose.yml

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    image: myregistry/saas-backend:1.0.0
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      JWT_SECRET: ${JWT_SECRET}
      DEBUG: "false"
    restart: always
    depends_on:
      - postgres

  frontend:
    image: myregistry/saas-frontend:1.0.0
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
```

## Kubernetes Deployment

### Create Namespace

```bash
kubectl create namespace saas
```

### Create Secrets

```bash
kubectl create secret generic saas-secrets \
  --from-literal=JWT_SECRET=your-secret \
  --from-literal=DB_PASSWORD=your-password \
  -n saas
```

### Deploy Services

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: saas-backend
  namespace: saas
spec:
  replicas: 2
  selector:
    matchLabels:
      app: saas-backend
  template:
    metadata:
      labels:
        app: saas-backend
    spec:
      containers:
      - name: backend
        image: myregistry/saas-backend:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: saas-secrets
              key: JWT_SECRET
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: saas-secrets
              key: GEMINI_API_KEY
        - name: DATABASE_URL
          value: postgresql+asyncpg://postgres:password@postgres:5432/saas_db
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## AWS Deployment

### RDS for Database

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier saas-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --master-username postgres \
  --master-user-password ${DB_PASSWORD}
```

### ECS for Containers

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name saas

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster saas \
  --service-name saas-backend \
  --task-definition saas-backend \
  --desired-count 2
```

### Application Load Balancer

```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name saas-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx
```

## CI/CD Pipeline

### GitHub Actions (Already Configured)

The project includes GitHub Actions workflows:
- `backend-ci.yml` - Backend tests and linting
- `frontend-ci.yml` - Frontend build and tests
- `docker-build.yml` - Docker image builds

### Manual Deployment Steps

```bash
# 1. Push to main branch
git push origin main

# 2. GitHub Actions runs tests
# 3. Build and push images
# 4. Deploy to production environment
```

## Monitoring & Logging

### Application Monitoring

```bash
# Add to requirements.txt
pip install prometheus-client

# Add to FastAPI
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

### Logging

```bash
# Add to requirements.txt
pip install python-json-logger

# Configure logging
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
```

### Error Tracking

```bash
# Add to requirements.txt
pip install sentry-sdk

# Initialize in app
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=0.1
)
```

## Database Backup

### Automated Backups

```bash
#!/bin/bash
# backup.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="saas_db_backup_${TIMESTAMP}.sql"

pg_dump -h localhost -U postgres saas_db > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://saas-backups/
```

Schedule with cron:
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

## SSL/TLS Configuration

### Let's Encrypt with Nginx

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Configure Nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
}
```

## Performance Optimization

### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_workspace_members_user_id ON workspace_members(user_id);
CREATE INDEX idx_projects_workspace_id ON projects(workspace_id);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM projects WHERE workspace_id = 'xxx';
```

### Caching Strategy

```python
# Add Redis caching
pip install redis aioredis

from aioredis import Redis

redis = await Redis.create_redis_pool('redis://localhost')
```

## Health Checks

### Endpoint Health Check

```bash
curl http://localhost:8000/health

# Expected: {"status":"ok"}
```

### Database Health Check

```bash
psql -U postgres -h localhost saas_db -c "SELECT 1;"
```

## Rollback Procedure

### Quick Rollback

```bash
# Stop current deployment
docker-compose down

# Deploy previous version
docker pull myregistry/saas-backend:1.0.0
docker-compose -f docker-compose.prod.yml up -d

# Verify
curl http://localhost:8000/health
```

### Database Rollback

```bash
# Restore from backup
pg_restore -d saas_db saas_db_backup_20240201_020000.sql

# Or using migration tool
alembic downgrade -1
```

## Support & Troubleshooting

### Common Issues

**Container won't start:**
```bash
docker logs <container-id>
docker inspect <container-id>
```

**Database connection error:**
```bash
psql -h localhost -U postgres -d saas_db
```

**High CPU usage:**
```bash
docker stats
# Identify container with high CPU
docker exec <container-id> top
```

### Getting Help

- Check logs: `docker-compose logs -f`
- Monitor resources: `docker stats`
- Health endpoint: `curl http://localhost:8000/health`
- Check documentation: See `/docs` folder
