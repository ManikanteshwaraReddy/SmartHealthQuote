# Deployment Guide for SmartHealthQuote Backend

This guide covers deployment options for your FastAPI backend across different platforms.

## 🚀 Deployment Options

### 1. **Local Development** (Docker Compose)
- Best for: Development, testing, demo
- Complexity: Low
- Cost: Free

### 2. **Cloud Platforms** (AWS, GCP, Azure)
- Best for: Production, scalability
- Complexity: Medium-High
- Cost: Variable

### 3. **Platform as a Service** (Heroku, Railway, Render)
- Best for: MVP, quick deployment
- Complexity: Low
- Cost: Low-Medium

### 4. **Serverless** (AWS Lambda, Vercel Functions)
- Best for: Lightweight APIs, cost optimization
- Complexity: Medium
- Cost: Very Low

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - DATABASE_URL=postgresql://user:password@db:5432/smarthealth
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=smarthealth
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Scale API service
docker-compose up -d --scale api=3

# Stop services
docker-compose down
```

## ☁️ AWS Deployment

### Option 1: AWS ECS (Recommended)

```yaml
# task-definition.json
{
  "family": "smarthealth-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-ecr-repo/smarthealth-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/smarthealth-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Deploy script:
```bash
#!/bin/bash
# deploy-aws.sh

# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

docker build -t smarthealth-api .
docker tag smarthealth-api:latest your-account.dkr.ecr.us-east-1.amazonaws.com/smarthealth-api:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/smarthealth-api:latest

# Update ECS service
aws ecs update-service --cluster smarthealth-cluster --service smarthealth-api --force-new-deployment
```

### Option 2: AWS Lambda (Serverless)

```python
# lambda_handler.py
from mangum import Mangum
from main import app

handler = Mangum(app)
```

```yaml
# serverless.yml
service: smarthealth-api

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    DATABASE_URL: ${env:DATABASE_URL}
    OPENAI_API_KEY: ${env:OPENAI_API_KEY}

functions:
  api:
    handler: lambda_handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 1024

plugins:
  - serverless-python-requirements
```

## 🌐 Platform as a Service Deployment

### Heroku

```yaml
# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# runtime.txt
python-3.11.6

# heroku.yml
build:
  docker:
    web: Dockerfile
```

Deploy commands:
```bash
# Create Heroku app
heroku create smarthealth-api

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main

# Scale
heroku ps:scale web=2
```

### Railway

```toml
# railway.toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "always"

[env]
DATABASE_URL = "${{DATABASE_URL}}"
OPENAI_API_KEY = "${{OPENAI_API_KEY}}"
```

Deploy:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: smarthealth-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: smarthealth-db
          property: connectionString
databases:
  - name: smarthealth-db
    databaseName: smarthealth
    user: smarthealth_user
```

## 📊 Production Configuration

### Environment Variables

```bash
# Production .env
DEBUG=false
CORS_ORIGINS=["https://yourfrontend.com"]
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
OPENAI_API_KEY=sk-your-key
SECRET_KEY=super-secure-key-in-production

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO

# Performance
MAX_WORKERS=4
WORKER_TIMEOUT=30
KEEPALIVE=2
```

### Production Settings

```python
# app/core/config.py
class ProductionSettings(Settings):
    debug: bool = False
    cors_origins: List[str] = ["https://yourfrontend.com"]
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = 20
    database_max_overflow: int = 30
    
    # Redis for caching
    redis_url: str = Field(..., env="REDIS_URL")
    cache_ttl: int = 3600
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = 15
    
    # Performance
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    worker_timeout: int = Field(default=30, env="WORKER_TIMEOUT")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
```

### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://api/health;
            access_log off;
        }
    }
}
```

## 📊 Monitoring & Logging

### Application Monitoring

```python
# app/core/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.core.config import settings

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
    )

# Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator

def setup_metrics(app):
    Instrumentator().instrument(app).expose(app)
```

### Structured Logging

```python
# app/core/logging.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        return json.dumps(log_entry)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, settings.log_level))
```

## 🔧 Database Migrations

```python
# migrations/versions/001_initial.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'insurance_policies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('policy_id', sa.String(50), unique=True),
        sa.Column('name', sa.String(255)),
        sa.Column('provider', sa.String(255)),
        sa.Column('data', sa.JSON),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    op.drop_table('insurance_policies')
```

## 🚀 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest
      
      - name: Run linting
        run: |
          pip install black flake8
          black --check .
          flake8 .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build and push Docker image
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
          docker build -t smarthealth-api .
          docker tag smarthealth-api:latest ${{ secrets.ECR_REGISTRY }}/smarthealth-api:latest
          docker push ${{ secrets.ECR_REGISTRY }}/smarthealth-api:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster smarthealth-cluster --service smarthealth-api --force-new-deployment
```

## 🎯 Post-Deployment Checklist

- [ ] **Health Check**: Verify `/health` endpoint returns 200
- [ ] **API Documentation**: Check `/docs` is accessible
- [ ] **Database**: Confirm database connection and migrations
- [ ] **Environment Variables**: Verify all secrets are set
- [ ] **SSL Certificate**: Ensure HTTPS is working
- [ ] **Domain**: Test custom domain if applicable
- [ ] **Monitoring**: Check logs and metrics
- [ ] **Load Testing**: Verify performance under load
- [ ] **Backup**: Ensure database backups are configured

## 🔍 Troubleshooting

### Common Issues

**Container Won't Start**:
```bash
# Check logs
docker logs container-name

# Check environment variables
docker exec container-name env

# Test locally
docker run -it --rm your-image bash
```

**Database Connection Failed**:
```bash
# Test connection
psql $DATABASE_URL

# Check network
docker network ls
```

**High Memory Usage**:
```python
# Monitor memory in code
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Load balancer (ALB, Nginx)
- Multiple API instances
- Database read replicas
- Redis for session storage

### Vertical Scaling
- Increase CPU/memory
- Optimize database queries
- Implement caching
- Async processing

Your backend is now ready for production deployment!